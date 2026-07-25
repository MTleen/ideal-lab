import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


PROFILE_PATH = Path(__file__).resolve().parents[1] / "profiles" / "development.json"


def validation_assignment(candidate_hash="sha256:candidate"):
    lease_token = "review-lease"
    return {
        "role": "validation",
        "goal_revision": "sha256:goal-r1",
        "phase": "implementation",
        "task_id": "validate",
        "produces": ["evidence://validation-pass"],
        "lease_token_hash": loop_kernel.content_ref(lease_token),
        "capability": {
            "id": "focused-validation",
            "locator": "worker:validate",
            "version": "1.0.0",
        },
        "candidate_hash": candidate_hash,
        "criteria_hash": "sha256:criteria",
        "input_hashes": ["sha256:source"],
        "review_kind": "terminal",
        "validation_fingerprint": "sha256:validator-v1",
    }


class ReviewBudgetTests(unittest.TestCase):
    def test_unchanged_candidate_reuses_passing_validation_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            record = validation_assignment()
            loop_kernel._reserve_assignment(root, record)
            started = loop_kernel.begin_run(
                root,
                record,
                "validation",
                lease_token="review-lease",
            )
            finished = loop_kernel.finish_run(
                root,
                started["run_id"],
                "completed",
                [],
                ["evidence://validation-pass"],
                validation_conclusion="pass",
            )

            reusable = loop_kernel.find_reusable_evidence(
                root,
                "sha256:candidate",
                "sha256:criteria",
                ["sha256:source"],
                "sha256:validator-v1",
            )
            changed = loop_kernel.find_reusable_evidence(
                root,
                "sha256:changed",
                "sha256:criteria",
                ["sha256:source"],
                "sha256:validator-v1",
            )
            changed_validator = loop_kernel.find_reusable_evidence(
                root,
                "sha256:candidate",
                "sha256:criteria",
                ["sha256:source"],
                "sha256:validator-v2",
            )

            self.assertEqual(reusable["run_id"], finished["run_id"])
            self.assertIsNone(changed)
            self.assertIsNone(changed_validator)

    def test_terminal_review_budget_defaults_to_one_per_candidate(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        prior = [
            {
                "role": "validation",
                "review_kind": "terminal",
                "candidate_hash": "sha256:candidate",
                "outcome": "failed",
            }
        ]

        self.assertFalse(
            loop_kernel.review_allowed(
                profile, "sha256:candidate", prior
            )
        )
        self.assertTrue(
            loop_kernel.review_allowed(profile, "sha256:changed", prior)
        )

    def test_review_finding_creates_only_a_substantive_execution_repair(self):
        assignment = loop_kernel.create_repair_assignment(
            {
                "finding_id": "F-1",
                "candidate_hash": "sha256:candidate",
                "affected_artifact": "artifact://draft",
                "repair_capability": "code-implementation",
                "summary": "Correct the stale behavior",
            },
            goal_revision="sha256:goal-r1",
            phase="implementation",
        )

        self.assertEqual(assignment["role"], "execution")
        self.assertEqual(
            assignment["capability_requirement"],
            "code-implementation",
        )
        self.assertEqual(assignment["task_kind"], "substantive_repair")
        self.assertNotEqual(assignment["task_kind"], "review")


if __name__ == "__main__":
    unittest.main()
