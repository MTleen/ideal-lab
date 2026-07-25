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
ARTIFACT_GRAPH = {
    "source-material": {"depends_on": [], "kind": "business"},
    "draft-artifact": {
        "depends_on": ["source-material"],
        "kind": "business",
    },
    "review-evidence": {
        "depends_on": ["draft-artifact"],
        "kind": "evidence",
    },
    "reviewer-config": {"depends_on": [], "kind": "reviewer"},
    "run-ledger": {"depends_on": [], "kind": "ledger"},
    "render-format": {"depends_on": [], "kind": "format"},
}


def completed_plan():
    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    goal = {
        "id": "DOC-001",
        "revision": "sha256:goal-r1",
        "phase": {"current": "draft", "next_gate": "draft-verified"},
    }
    plan = loop_kernel.derive_task_plan(
        goal,
        profile,
        ["draft-artifact", "review-evidence"],
    )
    return plan


class InvalidationTests(unittest.TestCase):
    def test_business_input_change_invalidates_only_downstream_artifacts(self):
        invalidated = loop_kernel.invalidate(
            completed_plan(), ["source-material"], ARTIFACT_GRAPH
        )

        self.assertEqual(
            invalidated["invalidation"]["invalidated_refs"],
            [
                "source-material",
                "draft-artifact",
                "review-evidence",
            ],
        )
        self.assertEqual(
            [task["status"] for task in invalidated["tasks"]],
            ["pending", "pending"],
        )

    def test_reviewer_ledger_and_format_changes_do_not_invalidate_business(self):
        for changed in ("reviewer-config", "run-ledger", "render-format"):
            with self.subTest(changed=changed):
                result = loop_kernel.invalidate(
                    completed_plan(), [changed], ARTIFACT_GRAPH
                )

                self.assertEqual(
                    result["invalidation"]["invalidated_refs"], []
                )
                self.assertEqual(
                    [task["status"] for task in result["tasks"]],
                    ["completed", "completed"],
                )
                self.assertEqual(
                    result["invalidation"]["ignored_refs"], [changed]
                )


if __name__ == "__main__":
    unittest.main()
