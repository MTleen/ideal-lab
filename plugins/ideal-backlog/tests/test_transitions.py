import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


ONE_GOAL_FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "one-goal-backlog.json"
)


def claim_one_goal(root, prefix):
    initial = ideal_backlog.init_store(root)
    snapshot = json.loads(ONE_GOAL_FIXTURE.read_text(encoding="utf-8"))
    seeded = ideal_backlog.write_revision(
        root,
        snapshot,
        expected_revision=initial["revision"],
        operation_id=prefix + "-seed",
    )
    claimed = ideal_backlog.claim_goal(
        root,
        "REQ-001",
        expected_revision=seeded["revision"],
        operation_id=prefix + "-claim",
    )
    return claimed, claimed["snapshot"]["goals"][0]["lease"]["token"]


def quality_transition(
    root,
    state,
    lease,
    operation_id,
    status,
    authority="runner",
    evidence_refs=None,
    reopen=None,
):
    patch = {"quality": {"status": status}}
    execution_for_quality = {
        "implemented": "executing",
        "verified": "verifying",
        "awaiting_acceptance": "awaiting_acceptance",
    }
    if status in execution_for_quality:
        patch["execution"] = {
            "status": execution_for_quality[status]
        }
    if reopen is not None:
        patch["reopen"] = reopen
    return ideal_backlog.transition_goal(
        root,
        "REQ-001",
        expected_revision=state["revision"],
        lease_token=lease,
        operation_id=operation_id,
        patch=patch,
        authority=authority,
        transition_reason="test transition",
        evidence_refs=evidence_refs or [],
    )


class TransitionPolicyTests(unittest.TestCase):
    def test_state_tables_declare_every_v2_state(self):
        self.assertEqual(
            set(ideal_backlog.EXECUTION_TRANSITIONS),
            {
                "todo",
                "claimed",
                "planning",
                "executing",
                "verifying",
                "awaiting_acceptance",
                "done",
                "blocked",
                "waiting",
                "human_gate",
                "cancelled",
            },
        )
        self.assertEqual(
            set(ideal_backlog.QUALITY_TRANSITIONS),
            {
                "unverified",
                "implemented",
                "verified",
                "awaiting_acceptance",
                "accepted",
                "legacy_accepted",
                "reopened",
            },
        )

    def test_transition_rejects_protected_goal_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, lease = claim_one_goal(root, "protected")

            for protected_patch in (
                {"id": "TAKEOVER"},
                {"lease": None},
                {"revision": "forged"},
                {"history_refs": []},
                {"acceptance": {"allowed_authorities": ["runner"]}},
            ):
                with self.subTest(patch=protected_patch):
                    with self.assertRaises(ideal_backlog.InvalidTransition):
                        ideal_backlog.transition_goal(
                            root,
                            "REQ-001",
                            expected_revision=state["revision"],
                            lease_token=lease,
                            operation_id="protected-{0}".format(
                                next(iter(protected_patch))
                            ),
                            patch=protected_patch,
                        )

    def test_acceptance_requires_allowed_authority_and_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, lease = claim_one_goal(root, "accept")
            state = quality_transition(
                root, state, lease, "accept-implemented", "implemented"
            )
            state = quality_transition(
                root, state, lease, "accept-verified", "verified"
            )
            state = quality_transition(
                root,
                state,
                lease,
                "accept-awaiting",
                "awaiting_acceptance",
            )

            with self.assertRaises(ideal_backlog.InvalidTransition):
                ideal_backlog.accept_goal(
                    root,
                    "REQ-001",
                    state["revision"],
                    "accept-runner",
                    "runner",
                    evidence_refs=["evidence://acceptance"],
                )
            with self.assertRaises(ideal_backlog.InvalidTransition):
                ideal_backlog.accept_goal(
                    root,
                    "REQ-001",
                    state["revision"],
                    "accept-no-evidence",
                    "human",
                    evidence_refs=[],
                )
            accepted = ideal_backlog.accept_goal(
                root,
                "REQ-001",
                state["revision"],
                "accept-human",
                "human",
                evidence_refs=["evidence://acceptance"],
            )

            self.assertEqual(
                accepted["snapshot"]["goals"][0]["quality"]["status"],
                "accepted",
            )

    def test_legacy_accepted_can_be_reopened_without_execution_lease(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initial = ideal_backlog.init_store(root)
            snapshot = json.loads(
                ONE_GOAL_FIXTURE.read_text(encoding="utf-8")
            )
            goal = snapshot["goals"][0]
            goal["execution"]["status"] = "done"
            goal["quality"]["status"] = "legacy_accepted"
            goal["quality"]["legacy"] = True
            seeded = ideal_backlog.write_revision(
                root,
                snapshot,
                expected_revision=initial["revision"],
                operation_id="legacy-seed",
            )

            reopened = ideal_backlog.reopen_goal(
                root,
                "REQ-001",
                expected_revision=seeded["revision"],
                operation_id="legacy-reopen",
                authority="human",
                reopen={
                    "reason": "regression",
                    "missing_test_reason": "legacy gap",
                    "required_regression": "cover migrated behavior",
                },
            )

            goal = reopened["snapshot"]["goals"][0]
            self.assertEqual(goal["execution"]["status"], "todo")
            self.assertEqual(goal["quality"]["status"], "reopened")

    def test_verified_cannot_skip_awaiting_acceptance(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, lease = claim_one_goal(root, "skip")
            state = quality_transition(
                root, state, lease, "skip-implemented", "implemented"
            )
            state = quality_transition(
                root, state, lease, "skip-verified", "verified"
            )

            with self.assertRaises(ideal_backlog.InvalidTransition):
                quality_transition(
                    root,
                    state,
                    lease,
                    "skip-accepted",
                    "accepted",
                    authority="human",
                    evidence_refs=["evidence://acceptance"],
                )

    def test_reopen_requires_reason_missing_test_and_regression(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, lease = claim_one_goal(root, "reopen")
            for operation_id, status in (
                ("reopen-implemented", "implemented"),
                ("reopen-verified", "verified"),
                ("reopen-awaiting", "awaiting_acceptance"),
            ):
                state = quality_transition(
                    root, state, lease, operation_id, status
                )
            state = ideal_backlog.accept_goal(
                root,
                "REQ-001",
                state["revision"],
                "reopen-accepted",
                "human",
                evidence_refs=["evidence://acceptance"],
            )

            with self.assertRaises(ideal_backlog.InvalidTransition):
                ideal_backlog.reopen_goal(
                    root,
                    "REQ-001",
                    state["revision"],
                    "reopen-incomplete",
                    "human",
                    reopen={"reason": "regression"},
                )
            reopened = ideal_backlog.reopen_goal(
                root,
                "REQ-001",
                state["revision"],
                "reopen-complete",
                "human",
                reopen={
                    "reason": "regression",
                    "missing_test_reason": "boundary was not covered",
                    "required_regression": "cover the failing boundary",
                },
            )

            self.assertEqual(
                reopened["snapshot"]["goals"][0]["quality"]["status"],
                "reopened",
            )
            self.assertEqual(
                reopened["snapshot"]["goals"][0][
                    "reopen_history"
                ][-1]["reason"],
                "regression",
            )

    def test_non_running_execution_states_release_the_lease(self):
        for terminal_status in ("blocked", "waiting", "human_gate"):
            with self.subTest(status=terminal_status):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    state, lease = claim_one_goal(root, terminal_status)

                    transitioned = ideal_backlog.transition_goal(
                        root,
                        "REQ-001",
                        expected_revision=state["revision"],
                        lease_token=lease,
                        operation_id=terminal_status + "-transition",
                        patch={
                            "execution": {"status": terminal_status},
                            "blocker": {
                                "reason": terminal_status,
                                "release_condition": "external change",
                            },
                        },
                        transition_reason="release the execution slot",
                    )

                    goal = transitioned["snapshot"]["goals"][0]
                    self.assertEqual(
                        goal["execution"]["status"], terminal_status
                    )
                    self.assertIsNone(goal["lease"])

    def test_cancelled_is_never_projected_as_done(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state, lease = claim_one_goal(root, "cancel")

            cancelled = ideal_backlog.transition_goal(
                root,
                "REQ-001",
                expected_revision=state["revision"],
                lease_token=lease,
                operation_id="cancel-transition",
                patch={"execution": {"status": "cancelled"}},
                transition_reason="cancelled by authority",
            )

            self.assertEqual(
                cancelled["snapshot"]["goals"][0]["execution"]["status"],
                "cancelled",
            )
            self.assertIsNone(cancelled["snapshot"]["goals"][0]["lease"])


if __name__ == "__main__":
    unittest.main()
