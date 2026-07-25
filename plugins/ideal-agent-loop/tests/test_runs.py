import copy
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


def assignment():
    lease_token = "lease-token"
    return {
        "role": "execution",
        "goal_revision": "sha256:goal-r1",
        "phase": "draft",
        "task_id": "compose",
        "produces": ["artifact://draft"],
        "lease_token_hash": loop_kernel.content_ref(lease_token),
        "capability": {
            "id": "compose",
            "locator": "worker:compose",
            "version": "1.0.0",
        },
        "candidate_hash": "sha256:candidate",
        "criteria_hash": "sha256:criteria",
        "input_hashes": ["sha256:source"],
        "review_kind": "terminal",
        "validation_fingerprint": "sha256:validator-v1",
    }


def begin_reserved(root, record, role, lease_token="lease-token"):
    loop_kernel._reserve_assignment(root, record)
    return loop_kernel.begin_run(
        root, record, role, lease_token=lease_token
    )


class RunEnvelopeTests(unittest.TestCase):
    def test_begin_records_assignment_identity_and_worker(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            run = begin_reserved(
                Path(temp_dir),
                assignment(),
                "execution",
            )

            self.assertTrue(run["run_id"])
            self.assertEqual(run["role"], "execution")
            self.assertEqual(run["goal_revision"], "sha256:goal-r1")
            self.assertEqual(run["phase"], "draft")
            self.assertEqual(run["task_id"], "compose")
            self.assertTrue(run["assignment_hash"].startswith("sha256:"))
            self.assertEqual(run["worker"]["locator"], "worker:compose")
            self.assertEqual(run["outcome"], "running")

    def test_finish_creates_an_immutable_terminal_record(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            started = begin_reserved(
                root,
                assignment(),
                "execution",
            )

            finished = loop_kernel.finish_run(
                root,
                started["run_id"],
                "completed",
                ["artifact://draft"],
                [],
            )
            finish_path = (
                root
                / ".ideal"
                / "loop"
                / "runs"
                / started["run_id"]
                / "finish.json"
            )
            original = finish_path.read_bytes()

            with self.assertRaises(loop_kernel.ImmutableRecordError):
                loop_kernel.finish_run(
                    root,
                    started["run_id"],
                    "failed",
                    [],
                    [],
                    root_cause="late overwrite",
                )
            self.assertEqual(finish_path.read_bytes(), original)
            self.assertEqual(finished["outcome"], "completed")
            self.assertEqual(finished["artifact_refs"], ["artifact://draft"])

    def test_execution_cannot_write_validation_conclusion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            started = begin_reserved(
                root,
                assignment(),
                "execution",
            )

            with self.assertRaises(loop_kernel.AuthorityError):
                loop_kernel.finish_run(
                    root,
                    started["run_id"],
                    "completed",
                    ["artifact://draft"],
                    [],
                    validation_conclusion="pass",
                )

    def test_execution_cannot_write_validation_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            started = begin_reserved(
                root,
                assignment(),
                "execution",
            )

            with self.assertRaises(loop_kernel.AuthorityError):
                loop_kernel.finish_run(
                    root,
                    started["run_id"],
                    "completed",
                    ["artifact://draft"],
                    ["evidence://forged-validation"],
                )

    def test_validation_cannot_return_modified_candidate_artifacts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            validation_assignment = copy.deepcopy(assignment())
            validation_assignment["task_id"] = "validate"
            validation_assignment["role"] = "validation"
            validation_assignment["produces"] = ["evidence://validation"]
            started = begin_reserved(
                root,
                validation_assignment,
                "validation",
            )

            with self.assertRaises(loop_kernel.AuthorityError):
                loop_kernel.finish_run(
                    root,
                    started["run_id"],
                    "completed",
                    ["artifact://modified-candidate"],
                    ["evidence://validation"],
                    validation_conclusion="pass",
                )

    def test_assignment_role_must_match_the_started_run_role(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            mismatched = assignment()
            mismatched["role"] = "validation"

            with self.assertRaises(loop_kernel.AuthorityError):
                begin_reserved(
                    Path(temp_dir),
                    mismatched,
                    "execution",
                )

    def test_run_requires_the_assignment_lease_and_declared_outputs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with self.assertRaises(loop_kernel.AuthorityError):
                begin_reserved(
                    Path(temp_dir),
                    assignment(),
                    "execution",
                    lease_token="different-token",
                )

    def test_assignment_reservation_can_be_consumed_only_once(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            record = assignment()
            loop_kernel._reserve_assignment(root, record)
            loop_kernel.begin_run(
                root,
                record,
                "execution",
                lease_token="lease-token",
            )

            with self.assertRaises(loop_kernel.AuthorityError):
                loop_kernel.begin_run(
                    root,
                    record,
                    "execution",
                    lease_token="lease-token",
                )

    def test_completed_validation_requires_pass_and_evidence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            validation_assignment = copy.deepcopy(assignment())
            validation_assignment["task_id"] = "validate"
            validation_assignment["role"] = "validation"
            validation_assignment["produces"] = ["evidence://validation"]
            started = begin_reserved(
                root,
                validation_assignment,
                "validation",
            )

            with self.assertRaises(loop_kernel.AuthorityError):
                loop_kernel.finish_run(
                    root,
                    started["run_id"],
                    "completed",
                    [],
                    ["evidence://validation"],
                    validation_conclusion="fail",
                )


if __name__ == "__main__":
    unittest.main()
