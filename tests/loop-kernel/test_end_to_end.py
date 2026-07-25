import copy
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKLOG = REPO_ROOT / "plugins" / "ideal-backlog"
LOOP = REPO_ROOT / "plugins" / "ideal-agent-loop"
sys.path.insert(0, str(BACKLOG / "scripts"))
sys.path.insert(0, str(LOOP / "scripts"))

import ideal_backlog  # noqa: E402
import loop_kernel  # noqa: E402


FIXTURES = Path(__file__).resolve().parent / "fixtures"
V1_SOURCE = FIXTURES / "v1" / "需求池.md"
DEVELOPMENT_PROFILE = LOOP / "profiles" / "development.json"
DOCUMENT_PROFILE = LOOP / "tests" / "fixtures" / "document-profile.json"


def seed(root):
    ideal_backlog.migrate_v1(
        root,
        V1_SOURCE,
        apply=True,
        operation_id="golden-migrate",
    )
    return ideal_backlog.read_current(root)


def claim(root):
    current = seed(root)
    return ideal_backlog.claim_goal(
        root,
        "REQ-GOLD",
        current["revision"],
        "golden-claim",
    )


def inspected(root):
    return loop_kernel.inspect_backlog_cli(
        BACKLOG / "scripts" / "ideal_backlog.py",
        root,
        goal_id="REQ-GOLD",
    )


def advance_to_awaiting(root, state, lease, prefix):
    state = ideal_backlog.transition_goal(
        root,
        "REQ-GOLD",
        state["revision"],
        lease,
        prefix + "-implemented",
        {
            "execution": {"status": "executing"},
            "quality": {"status": "implemented"},
        },
        transition_reason="candidate implemented",
        evidence_refs=["evidence://execution"],
    )
    state = ideal_backlog.transition_goal(
        root,
        "REQ-GOLD",
        state["revision"],
        lease,
        prefix + "-verified",
        {
            "execution": {"status": "verifying"},
            "quality": {"status": "verified"},
        },
        transition_reason="validation passed",
        evidence_refs=["evidence://validation"],
    )
    return ideal_backlog.transition_goal(
        root,
        "REQ-GOLD",
        state["revision"],
        lease,
        prefix + "-awaiting",
        {
            "execution": {"status": "awaiting_acceptance"},
            "quality": {"status": "awaiting_acceptance"},
        },
        transition_reason="awaiting acceptance authority",
    )


class LoopKernelGoldenScenarios(unittest.TestCase):
    def test_v1_migration_is_dry_run_auditable_and_mirrored(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            preview = ideal_backlog.migrate_v1(
                root, V1_SOURCE, apply=False
            )
            self.assertFalse((root / ".ideal").exists())

            applied = seed(root)

            self.assertTrue(preview["can_apply"])
            self.assertEqual(len(applied["snapshot"]["goals"]), 1)
            self.assertTrue(
                (
                    root
                    / applied["snapshot"]["metadata"]["migration"][
                        "source_snapshot_ref"
                    ]
                ).is_file()
            )
            self.assertTrue(
                ideal_backlog.verify_mirror(
                    root, root / "docs" / "dev" / "需求池.md"
                )["matches"]
            )

    def test_fixed_goal_completes_two_dependent_tasks_with_separate_runs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            claimed = claim(root)
            lease = claimed["snapshot"]["goals"][0]["lease"]["token"]
            profile = loop_kernel.load_profile(DEVELOPMENT_PROFILE)
            capabilities = loop_kernel.load_capabilities(
                FIXTURES / "development" / "capabilities.json"
            )
            state = inspected(root)

            execution_step = loop_kernel.step_once(
                state,
                profile,
                capabilities,
                source_binding="fixed",
                goal_id="REQ-GOLD",
                lease_token=lease,
                loop_root=root,
            )
            execution = loop_kernel.begin_run(
                root,
                execution_step["assignment"],
                "execution",
                lease_token=lease,
            )
            execution = loop_kernel.finish_run(
                root,
                execution["run_id"],
                "completed",
                ["implementation-artifact"],
                [],
            )
            validation_step = loop_kernel.step_once(
                state,
                profile,
                capabilities,
                source_binding="fixed",
                goal_id="REQ-GOLD",
                prior_runs=[execution],
                lease_token=lease,
                loop_root=root,
            )
            validation = loop_kernel.begin_run(
                root,
                validation_step["assignment"],
                "validation",
                lease_token=lease,
            )
            validation = loop_kernel.finish_run(
                root,
                validation["run_id"],
                "completed",
                [],
                ["focused-test-evidence"],
                validation_conclusion="pass",
            )
            finished_step = loop_kernel.step_once(
                state,
                profile,
                capabilities,
                source_binding="fixed",
                goal_id="REQ-GOLD",
                prior_runs=[execution, validation],
                lease_token=lease,
                loop_root=root,
            )
            quality = claimed
            for index, intent in enumerate(
                finished_step["transition_sequence"], start=1
            ):
                quality = ideal_backlog.transition_goal(
                    root,
                    "REQ-GOLD",
                    quality["revision"],
                    lease,
                    "golden-gate-{0}".format(index),
                    intent["patch"],
                    transition_reason=intent["reason"],
                    evidence_refs=intent["evidence_refs"],
                )

            self.assertEqual(execution["role"], "execution")
            self.assertEqual(validation["role"], "validation")
            self.assertNotEqual(execution["run_id"], validation["run_id"])
            self.assertEqual(finished_step["outcome"], "gate_passed")
            self.assertEqual(
                quality["snapshot"]["goals"][0]["quality"]["status"],
                "awaiting_acceptance",
            )
            self.assertIsNone(
                quality["snapshot"]["goals"][0]["lease"]
            )

    def test_dynamic_goal_selection_honors_priority_deadline_fifo_and_dependencies(self):
        snapshot = {
            "goals": [
                {
                    "id": "DONE",
                    "priority": "P0",
                    "dependencies": [],
                    "execution": {"status": "done"},
                    "quality": {"status": "accepted"},
                },
                {
                    "id": "LATER",
                    "priority": "P1",
                    "deadline": "2026-08-02",
                    "created_at": "2026-06-01",
                    "dependencies": [],
                    "execution": {"status": "todo"},
                    "quality": {"status": "unverified"},
                },
                {
                    "id": "READY",
                    "priority": "P1",
                    "deadline": "2026-08-01",
                    "created_at": "2026-07-01",
                    "dependencies": ["DONE"],
                    "execution": {"status": "todo"},
                    "quality": {"status": "unverified"},
                },
            ]
        }

        self.assertEqual(
            loop_kernel.select_goal(snapshot, "dynamic")["id"], "READY"
        )

    def test_unchanged_validation_evidence_is_reused(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            assignment = {
                "role": "validation",
                "goal_revision": "sha256:goal",
                "phase": "draft",
                "task_id": "validate",
                "produces": ["evidence://pass"],
                "lease_token_hash": loop_kernel.content_ref("lease"),
                "capability": {
                    "id": "validate",
                    "locator": "mock:validate",
                    "version": "1.0.0",
                },
                "candidate_hash": "sha256:candidate",
                "criteria_hash": "sha256:criteria",
                "input_hashes": ["sha256:input"],
                "review_kind": "terminal",
                "validation_fingerprint": "sha256:validator-v1",
            }
            loop_kernel._reserve_assignment(root, assignment)
            run = loop_kernel.begin_run(
                root,
                assignment,
                "validation",
                lease_token="lease",
            )
            run = loop_kernel.finish_run(
                root,
                run["run_id"],
                "completed",
                [],
                ["evidence://pass"],
                validation_conclusion="pass",
            )

            reused = loop_kernel.find_reusable_evidence(
                root,
                "sha256:candidate",
                "sha256:criteria",
                ["sha256:input"],
                "sha256:validator-v1",
            )

            self.assertEqual(reused["run_id"], run["run_id"])

    def test_business_change_invalidates_downstream_not_reviewer_metadata(self):
        profile = loop_kernel.load_profile(DOCUMENT_PROFILE)
        goal = {
            "id": "DOC",
            "revision": "sha256:doc",
            "phase": {"current": "draft"},
            "lease": {
                "token": "doc-lease",
                "claimed_at": "2026-07-25T00:00:00Z",
            },
        }
        plan = loop_kernel.derive_task_plan(
            goal, profile, ["draft-artifact", "review-evidence"]
        )
        graph = {
            "source-material": {"depends_on": [], "kind": "business"},
            "draft-artifact": {
                "depends_on": ["source-material"],
                "kind": "business",
            },
            "review-evidence": {
                "depends_on": ["draft-artifact"],
                "kind": "evidence",
            },
            "reviewer-config": {
                "depends_on": [],
                "kind": "reviewer",
            },
        }

        changed = loop_kernel.invalidate(
            plan, ["source-material"], graph
        )
        metadata = loop_kernel.invalidate(
            plan, ["reviewer-config"], graph
        )

        self.assertEqual(
            changed["invalidation"]["invalidated_refs"],
            ["source-material", "draft-artifact", "review-evidence"],
        )
        self.assertEqual(
            metadata["invalidation"]["invalidated_refs"], []
        )

    def test_review_finding_is_substantive_repair_not_review_of_review(self):
        repair = loop_kernel.create_repair_assignment(
            {
                "finding_id": "F-1",
                "candidate_hash": "sha256:candidate",
                "affected_artifact": "artifact://candidate",
                "repair_capability": "content-composition",
                "summary": "Correct the candidate",
            },
            "sha256:goal",
            "draft",
        )

        self.assertEqual(repair["task_kind"], "substantive_repair")
        self.assertEqual(repair["role"], "execution")

    def test_third_same_root_cause_blocks_and_releases_slot(self):
        profile = loop_kernel.load_profile(DOCUMENT_PROFILE)
        goal = {
            "id": "DOC",
            "profile": "document",
            "revision": "sha256:doc",
            "priority": "P1",
            "dependencies": [],
            "execution": {"status": "todo"},
            "quality": {"status": "unverified"},
            "phase": {"current": "draft"},
            "lease": {
                "token": "doc-lease",
                "claimed_at": "2026-07-25T00:00:00Z",
            },
        }
        state = {
            "revision": "sha256:store",
            "snapshot": {"goals": [goal]},
        }
        failures = [
            {
                "goal_revision": "sha256:doc",
                "outcome": "failed",
                "root_cause": "same",
            }
            for _ in range(3)
        ]

        result = loop_kernel.step_once(
            state,
            profile,
            loop_kernel.load_capabilities(
                FIXTURES / "document" / "capabilities.json"
            ),
            "fixed",
            goal_id="DOC",
            prior_runs=failures,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertTrue(result["release_execution_slot"])

    def test_human_gate_releases_goal_lease(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            claimed = claim(root)
            lease = claimed["snapshot"]["goals"][0]["lease"]["token"]

            gated = ideal_backlog.transition_goal(
                root,
                "REQ-GOLD",
                claimed["revision"],
                lease,
                "golden-human-gate",
                {
                    "execution": {"status": "human_gate"},
                    "blocker": {
                        "reason": "approval required",
                        "release_condition": "authority responds",
                    },
                },
                transition_reason="external authority required",
            )

            self.assertIsNone(gated["snapshot"]["goals"][0]["lease"])

    def test_document_profile_runs_without_development_adapters(self):
        profile = loop_kernel.load_profile(DOCUMENT_PROFILE)
        goal = {
            "id": "DOC",
            "profile": "document",
            "revision": "sha256:doc",
            "priority": "P1",
            "dependencies": [],
            "execution": {"status": "todo"},
            "quality": {"status": "unverified"},
            "phase": {"current": "draft"},
            "lease": {
                "token": "doc-lease",
                "claimed_at": "2026-07-25T00:00:00Z",
            },
        }

        step = loop_kernel.step_once(
            {
                "revision": "sha256:store",
                "snapshot": {"goals": [goal]},
            },
            profile,
            loop_kernel.load_capabilities(
                FIXTURES / "document" / "capabilities.json"
            ),
            "fixed",
            goal_id="DOC",
            lease_token="doc-lease",
        )

        self.assertNotIn("adapters", profile)
        self.assertEqual(step["outcome"], "assignment")
        self.assertEqual(step["role"], "execution")

    def test_runner_cannot_accept_and_reopen_preserves_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            claimed = claim(root)
            lease = claimed["snapshot"]["goals"][0]["lease"]["token"]
            awaiting = advance_to_awaiting(
                root, claimed, lease, "golden-quality"
            )

            with self.assertRaises(ideal_backlog.InvalidTransition):
                ideal_backlog.accept_goal(
                    root,
                    "REQ-GOLD",
                    awaiting["revision"],
                    "golden-runner-accept",
                    "runner",
                    evidence_refs=["evidence://self"],
                )
            accepted = ideal_backlog.accept_goal(
                root,
                "REQ-GOLD",
                awaiting["revision"],
                "golden-human-accept",
                "human",
                evidence_refs=["evidence://acceptance"],
            )
            reopened = ideal_backlog.reopen_goal(
                root,
                "REQ-GOLD",
                accepted["revision"],
                "golden-reopen",
                "human",
                {
                    "reason": "counterevidence",
                    "missing_test_reason": "edge case absent",
                    "required_regression": "cover the edge case",
                },
            )
            goal_record = reopened["snapshot"]["goals"][0]

            self.assertIn(
                "evidence://acceptance", goal_record["evidence_refs"]
            )
            self.assertEqual(
                goal_record["reopen_history"][-1][
                    "required_regression"
                ],
                "cover the edge case",
            )


if __name__ == "__main__":
    unittest.main()
