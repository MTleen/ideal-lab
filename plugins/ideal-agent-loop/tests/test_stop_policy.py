import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


STOP_HOOK_PATH = SCRIPTS_DIR / "agent_loop_stop_hook.py"
SPEC = importlib.util.spec_from_file_location("agent_loop_stop_hook", STOP_HOOK_PATH)
stop_hook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(stop_hook)


class StopPolicyTests(unittest.TestCase):
    def test_continue_requires_ready_work_and_every_budget(self):
        self.assertTrue(
            loop_kernel.continue_running(
                ready_work_exists=True,
                status="executing",
                retry_budget_available=True,
                review_budget_available=True,
                permission_budget_available=True,
            )
        )
        for denied in (
            "retry_budget_available",
            "review_budget_available",
            "permission_budget_available",
        ):
            arguments = {
                "ready_work_exists": True,
                "status": "executing",
                "retry_budget_available": True,
                "review_budget_available": True,
                "permission_budget_available": True,
            }
            arguments[denied] = False
            with self.subTest(denied=denied):
                self.assertFalse(loop_kernel.continue_running(**arguments))

    def test_non_running_outcomes_never_continue(self):
        for status in (
            "blocked",
            "waiting",
            "human_gate",
            "no_op",
            "cancelled",
            "awaiting_acceptance",
        ):
            with self.subTest(status=status):
                self.assertFalse(
                    loop_kernel.continue_running(
                        ready_work_exists=True,
                        status=status,
                        retry_budget_available=True,
                        review_budget_available=True,
                        permission_budget_available=True,
                    )
                )

    def test_stop_hook_releases_at_awaiting_acceptance(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            task_dir = root / ".agent-loop" / "task"
            task_dir.mkdir(parents=True)
            state_path = task_dir / "state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "task": "task",
                        "iteration": 1,
                        "max_iterations": 20,
                        "status": "active",
                        "quality_required": True,
                        "quality_status": "verified",
                        "criteria": [
                            {"id": 1, "status": "passed"}
                        ],
                    }
                ),
                encoding="utf-8",
            )

            result = stop_hook.process_hook({"cwd": str(root)})
            saved = json.loads(state_path.read_text(encoding="utf-8"))

            self.assertIsNone(result)
            self.assertEqual(saved["status"], "awaiting_acceptance")

    def test_stop_hook_releases_waiting_and_budget_exhaustion(self):
        for state in (
            {
                "task": "waiting",
                "status": "waiting",
                "criteria": [{"id": 1, "status": "pending"}],
            },
            {
                "task": "budget",
                "status": "active",
                "criteria": [{"id": 1, "status": "pending"}],
                "budgets": {"retry_available": False},
            },
        ):
            with self.subTest(task=state["task"]):
                with tempfile.TemporaryDirectory() as temp_dir:
                    root = Path(temp_dir)
                    task_dir = root / ".agent-loop" / state["task"]
                    task_dir.mkdir(parents=True)
                    (task_dir / "state.json").write_text(
                        json.dumps(state), encoding="utf-8"
                    )

                    self.assertIsNone(
                        stop_hook.process_hook({"cwd": str(root)})
                    )

    def test_legacy_timestamp_without_authority_and_evidence_is_not_accepted(self):
        state = {
            "quality_required": True,
            "quality_status": "accepted",
            "acceptance": {"accepted_at": "2026-07-25T00:00:00Z"},
        }

        self.assertFalse(stop_hook._quality_accepted(state))

    def test_completed_unaccepted_state_with_no_criteria_normalizes_to_waiting(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            task_dir = root / ".agent-loop" / "empty"
            task_dir.mkdir(parents=True)
            state_path = task_dir / "state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "task": "empty",
                        "status": "completed",
                        "quality_required": True,
                        "quality_status": "verified",
                        "criteria": [],
                    }
                ),
                encoding="utf-8",
            )

            self.assertIsNone(stop_hook.process_hook({"cwd": str(root)}))
            saved = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(saved["status"], "awaiting_acceptance")


if __name__ == "__main__":
    unittest.main()
