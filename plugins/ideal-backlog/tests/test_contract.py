import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PLUGIN_ROOT / "schemas" / "goal-v2.schema.json"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SKILL_PATH = (
    PLUGIN_ROOT / "skills" / "ideal-backlog" / "SKILL.md"
)
REFERENCE_PATH = (
    PLUGIN_ROOT
    / "skills"
    / "ideal-backlog"
    / "references"
    / "goal-store-v2.md"
)

REQUIRED_GOAL_KEYS = {
    "id",
    "profile",
    "project_path",
    "source_binding",
    "priority",
    "dependencies",
    "execution",
    "quality",
    "phase",
    "revision",
    "lease",
    "evidence_refs",
    "history_refs",
}


class GoalContractTests(unittest.TestCase):
    def test_schema_declares_the_v2_goal_contract(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

        self.assertEqual(schema["$id"], "ideal-backlog/goal-v2")
        self.assertEqual(schema["type"], "object")
        self.assertEqual(set(schema["required"]), REQUIRED_GOAL_KEYS)

    def test_empty_backlog_fixture_uses_the_v2_envelope(self):
        fixture = json.loads(
            (FIXTURES_DIR / "empty-backlog.json").read_text(encoding="utf-8")
        )

        self.assertEqual(fixture["schema"], "ideal-backlog/backlog-v2")
        self.assertEqual(fixture["goals"], [])

    def test_one_goal_fixture_has_required_defaults(self):
        fixture = json.loads(
            (FIXTURES_DIR / "one-goal-backlog.json").read_text(encoding="utf-8")
        )
        goal = fixture["goals"][0]

        self.assertEqual(fixture["schema"], "ideal-backlog/backlog-v2")
        self.assertTrue(REQUIRED_GOAL_KEYS.issubset(goal))
        self.assertEqual(goal["execution"]["status"], "todo")
        self.assertEqual(goal["quality"]["status"], "unverified")

    def test_skill_contract_describes_the_v2_atomic_goal_store(self):
        skill = SKILL_PATH.read_text(encoding="utf-8")
        required_phrases = {
            "single machine source of truth",
            "expected revision",
            "lease token",
            "operation ID",
            "--apply",
            "fixed",
            "dynamic",
            "blocked",
            "waiting",
            "human_gate",
            "reopen",
        }

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)
        self.assertNotIn("事实源是 需求池.md", skill)
        self.assertTrue(REFERENCE_PATH.is_file())
        self.assertIn(
            "generated Markdown mirror",
            REFERENCE_PATH.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
