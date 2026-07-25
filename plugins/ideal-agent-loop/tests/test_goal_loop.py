import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


PROFILE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "document-profile.json"
)


def goal(
    goal_id,
    *,
    priority="P1",
    deadline=None,
    created_at="2026-07-01",
    dependencies=None,
    status="todo",
    quality="unverified",
    lease_token=None,
):
    record = {
        "id": goal_id,
        "profile": "document",
        "revision": "sha256:" + goal_id,
        "source_binding": "dynamic",
        "priority": priority,
        "deadline": deadline,
        "created_at": created_at,
        "dependencies": dependencies or [],
        "execution": {"status": status},
        "quality": {"status": quality},
        "phase": {"current": "draft", "next_gate": "draft-verified"},
    }
    record["lease"] = (
        None
        if lease_token is None
        else {"token": lease_token, "claimed_at": "2026-07-25T00:00:00Z"}
    )
    return record


def capabilities():
    return [
        {
            "schema": "ideal-agent-loop/capability-v1",
            "id": "content-composition",
            "locator": "worker:compose",
            "version": "1.0.0",
            "inputs": ["task-assignment", "source-material"],
            "outputs": ["draft-artifact"],
            "permissions": ["workspace-read", "workspace-write"],
            "verified": True,
        },
        {
            "schema": "ideal-agent-loop/capability-v1",
            "id": "content-validation",
            "locator": "worker:validate",
            "version": "1.0.0",
            "inputs": [
                "task-assignment",
                "draft-artifact",
                "criteria",
            ],
            "outputs": ["review-evidence"],
            "permissions": ["workspace-read"],
            "verified": True,
        },
    ]


class GoalLoopTests(unittest.TestCase):
    def test_fixed_binding_selects_only_the_named_goal(self):
        snapshot = {
            "goals": [
                goal("HIGH", priority="P0"),
                goal("FIXED", priority="P2"),
            ]
        }

        selected = loop_kernel.select_goal(
            snapshot, "fixed", goal_id="FIXED"
        )

        self.assertEqual(selected["id"], "FIXED")

    def test_dynamic_binding_uses_priority_deadline_and_fifo_after_dependencies(self):
        snapshot = {
            "goals": [
                goal(
                    "DONE",
                    priority="P0",
                    status="done",
                    quality="accepted",
                ),
                goal(
                    "BLOCKED-P0",
                    priority="P0",
                    status="blocked",
                ),
                goal(
                    "WAITING-DEP",
                    priority="P0",
                    dependencies=["MISSING"],
                ),
                goal(
                    "LATER",
                    deadline="2026-08-02",
                    created_at="2026-06-01",
                ),
                goal(
                    "READY",
                    deadline="2026-08-01",
                    created_at="2026-07-02",
                    dependencies=["DONE"],
                ),
            ]
        }

        selected = loop_kernel.select_goal(snapshot, "dynamic")

        self.assertEqual(selected["id"], "READY")

    def test_dynamic_binding_skips_an_already_leased_goal(self):
        leased = goal("LEASED", priority="P0")
        leased["lease"] = {"token": "held"}
        snapshot = {"goals": [leased, goal("READY", priority="P1")]}

        selected = loop_kernel.select_goal(snapshot, "dynamic")

        self.assertEqual(selected["id"], "READY")

    def test_stale_observation_requests_reload_before_assignment(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {"goals": [goal("FIXED")]},
        }

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
            observed_revision="sha256:stale",
        )

        self.assertEqual(result["outcome"], "reload")
        self.assertEqual(result["reason"], "stale_backlog_revision")

    def test_no_ready_work_is_a_no_op(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {
                "goals": [
                    goal("WAITING", status="waiting"),
                    goal("BLOCKED", status="blocked"),
                ]
            },
        }

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="dynamic",
        )

        self.assertEqual(result["outcome"], "no_op")
        self.assertTrue(result["release_execution_slot"])

    def test_third_consecutive_same_root_cause_blocks(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {"goals": [goal("FIXED")]},
        }
        prior_runs = [
            {
                "goal_revision": "sha256:FIXED",
                "outcome": "failed",
                "root_cause": "same-cause",
            }
            for _ in range(3)
        ]

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
            prior_runs=prior_runs,
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["reason"], "same_root_cause_exhausted")
        self.assertTrue(result["release_execution_slot"])

    def test_profile_mismatch_blocks_before_capability_routing(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        mismatched = goal("FIXED")
        mismatched["profile"] = "development"
        state = {
            "revision": "sha256:current",
            "snapshot": {"goals": [mismatched]},
        }

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["reason"], "profile_mismatch")

    def test_unleased_goal_requests_claim_before_assignment(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {"goals": [goal("FIXED")]},
        }

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
        )

        self.assertEqual(result["outcome"], "claim_required")
        self.assertEqual(result["claim"]["expected_revision"], "sha256:current")

    def test_failed_validation_evidence_does_not_satisfy_the_gate(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {
                "goals": [
                    goal(
                        "FIXED",
                        status="claimed",
                        lease_token="lease",
                    )
                ]
            },
        }
        runs = [
            {
                "task_id": "compose",
                "role": "execution",
                "goal_revision": "sha256:FIXED",
                "phase": "draft",
                "outcome": "completed",
                "artifact_refs": ["draft-artifact"],
                "evidence_refs": [],
            },
            {
                "task_id": "validate",
                "role": "validation",
                "goal_revision": "sha256:FIXED",
                "phase": "draft",
                "outcome": "completed",
                "artifact_refs": [],
                "evidence_refs": ["review-evidence"],
                "validation_conclusion": "fail",
            },
        ]

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
            prior_runs=runs,
            lease_token="lease",
        )

        self.assertEqual(result["outcome"], "assignment")
        self.assertEqual(result["assignment"]["task_id"], "validate")

    def test_passing_validation_produces_explicit_gate_intent(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {
                "goals": [
                    goal(
                        "FIXED",
                        status="claimed",
                        lease_token="lease",
                    )
                ]
            },
        }
        runs = [
            {
                "task_id": "compose",
                "role": "execution",
                "goal_revision": "sha256:FIXED",
                "phase": "draft",
                "outcome": "completed",
                "artifact_refs": ["draft-artifact"],
                "evidence_refs": [],
            },
            {
                "task_id": "validate",
                "role": "validation",
                "goal_revision": "sha256:FIXED",
                "phase": "draft",
                "outcome": "completed",
                "artifact_refs": [],
                "evidence_refs": ["review-evidence"],
                "validation_conclusion": "pass",
            },
        ]

        result = loop_kernel.step_once(
            state,
            profile,
            capabilities(),
            source_binding="fixed",
            goal_id="FIXED",
            prior_runs=runs,
            lease_token="lease",
        )

        self.assertEqual(result["outcome"], "gate_passed")
        self.assertEqual(
            [
                (
                    intent["patch"]["execution"]["status"],
                    intent["patch"]["quality"]["status"],
                )
                for intent in result["transition_sequence"]
            ],
            [
                ("executing", "implemented"),
                ("verifying", "verified"),
                ("awaiting_acceptance", "awaiting_acceptance"),
            ],
        )
        self.assertTrue(result["release_execution_slot"])

    def test_non_final_gate_advances_to_the_next_profile_phase(self):
        profile = json.loads(
            (
                Path(__file__).resolve().parents[1]
                / "profiles"
                / "development.json"
            ).read_text(encoding="utf-8")
        )
        selected_goal = goal(
            "FIXED", status="claimed", lease_token="lease"
        )
        selected_goal["profile"] = "development"
        selected_goal["phase"] = {
            "current": "requirement",
            "next_gate": "requirement-approved",
        }
        state = {
            "revision": "sha256:current",
            "snapshot": {"goals": [selected_goal]},
        }
        runs = [
            {
                "task_id": "requirement-baseline",
                "role": "execution",
                "goal_revision": "sha256:FIXED",
                "phase": "requirement",
                "outcome": "completed",
                "artifact_refs": ["requirement-baseline"],
                "evidence_refs": [],
            }
        ]

        result = loop_kernel.step_once(
            state,
            profile,
            [],
            source_binding="fixed",
            goal_id="FIXED",
            prior_runs=runs,
            lease_token="lease",
        )

        self.assertEqual(result["outcome"], "gate_passed")
        self.assertEqual(
            result["transition_intent"],
            {
                "patch": {
                    "phase": {
                        "current": "implementation",
                        "next_gate": "implementation-verified",
                    }
                },
                "reason": "advance_to_next_phase",
                "evidence_refs": ["requirement-baseline"],
            },
        )
        self.assertNotIn("transition_sequence", result)

    def test_assignment_reservation_prevents_duplicate_dispatch(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        state = {
            "revision": "sha256:current",
            "snapshot": {
                "goals": [goal("FIXED", lease_token="lease")]
            },
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            first = loop_kernel.step_once(
                state,
                profile,
                capabilities(),
                source_binding="fixed",
                goal_id="FIXED",
                lease_token="lease",
                loop_root=Path(temp_dir),
            )
            second = loop_kernel.step_once(
                state,
                profile,
                capabilities(),
                source_binding="fixed",
                goal_id="FIXED",
                lease_token="lease",
                loop_root=Path(temp_dir),
            )

        self.assertEqual(first["outcome"], "assignment")
        self.assertEqual(second["outcome"], "no_op")
        self.assertEqual(second["reason"], "assignment_reserved")


if __name__ == "__main__":
    unittest.main()
