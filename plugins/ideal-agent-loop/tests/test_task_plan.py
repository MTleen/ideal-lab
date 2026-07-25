import copy
import json
import sys
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


def goal():
    return {
        "id": "DOC-001",
        "revision": "sha256:goal-r1",
        "phase": {"current": "draft", "next_gate": "draft-verified"},
    }


class TaskPlanTests(unittest.TestCase):
    def test_plan_binds_to_goal_revision_and_phase_without_goal_status(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

        plan = loop_kernel.derive_task_plan(goal(), profile, [])

        self.assertEqual(plan["goal_revision"], "sha256:goal-r1")
        self.assertEqual(plan["phase"], "draft")
        self.assertNotIn("goal_status", plan)
        self.assertTrue(plan["plan_id"].startswith("sha256:"))

    def test_selects_exactly_one_dependency_satisfied_task(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        plan = loop_kernel.derive_task_plan(goal(), profile, [])

        first = loop_kernel.select_ready_task(plan)
        self.assertEqual(first["id"], "compose")

        checkpointed = loop_kernel.checkpoint(
            plan,
            {
                "run_id": "run-compose",
                "task_id": "compose",
                "outcome": "completed",
            },
            ["draft-artifact"],
        )
        second = loop_kernel.select_ready_task(checkpointed)

        self.assertEqual(second["id"], "validate")

    def test_checkpoint_returns_a_new_plan_with_immutable_reference(self):
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        plan = loop_kernel.derive_task_plan(goal(), profile, [])
        original = copy.deepcopy(plan)

        checkpointed = loop_kernel.checkpoint(
            plan,
            {
                "run_id": "run-compose",
                "task_id": "compose",
                "outcome": "completed",
            },
            ["draft-artifact"],
        )

        self.assertEqual(plan, original)
        self.assertTrue(
            checkpointed["checkpoints"][0]["ref"].startswith("sha256:")
        )
        self.assertEqual(
            checkpointed["tasks"][0]["status"], "completed"
        )


if __name__ == "__main__":
    unittest.main()
