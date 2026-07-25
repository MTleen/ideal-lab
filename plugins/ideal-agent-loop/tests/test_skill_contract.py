import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL = (
    PLUGIN_ROOT / "skills" / "ideal-agent-loop" / "SKILL.md"
)
REFERENCES = (
    PLUGIN_ROOT / "skills" / "ideal-agent-loop" / "references"
)


class SkillContractTests(unittest.TestCase):
    def test_skill_describes_the_bounded_profile_driven_kernel(self):
        text = SKILL.read_text(encoding="utf-8")
        required = {
            "Goal Loop",
            "Stage / Task Loop",
            "Loop Profile",
            "Capability Registry",
            "Execution Run",
            "Validation Run",
            "fixed",
            "dynamic",
            "waiting",
            "human_gate",
            "no_op",
            "review budget",
            "evidence reuse",
        }

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_skill_rejects_v1_unbounded_and_direct_state_write_language(self):
        text = SKILL.read_text(encoding="utf-8")

        for forbidden in (
            "循环不会自行停止",
            "所有验收标准通过前不允许停止",
            "状态流转的事实源是 需求池.md",
            "委托 ideal-dev-workflow 跑",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)
        self.assertIn(
            "ideal-backlog is the only machine Goal source of truth",
            text,
        )

    def test_references_align_with_runs_profiles_and_cooperative_stop(self):
        contract = (
            REFERENCES / "contract-template.md"
        ).read_text(encoding="utf-8")
        continuation = (
            REFERENCES / "continuation-template.md"
        ).read_text(encoding="utf-8")
        verification = (
            REFERENCES / "verification-guide.md"
        ).read_text(encoding="utf-8")
        config = (
            REFERENCES / "loop-config.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Goal revision", contract)
        self.assertIn("release the execution slot", continuation)
        self.assertIn("Validation Run", verification)
        self.assertIn("Profile JSON", config)
        self.assertNotIn("Do NOT stop", continuation)


if __name__ == "__main__":
    unittest.main()
