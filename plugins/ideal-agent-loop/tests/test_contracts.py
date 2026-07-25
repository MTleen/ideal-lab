import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = PLUGIN_ROOT / "schemas"
DEVELOPMENT_PROFILE = PLUGIN_ROOT / "profiles" / "development.json"
DOCUMENT_PROFILE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "document-profile.json"
)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class KernelContractTests(unittest.TestCase):
    def test_profile_and_capability_contracts_are_explicit(self):
        profile_schema = load_json(SCHEMAS / "profile-v1.schema.json")
        capability_schema = load_json(
            SCHEMAS / "capability-v1.schema.json"
        )

        self.assertEqual(
            profile_schema["$id"], "ideal-agent-loop/profile-v1"
        )
        self.assertTrue(
            {
                "schema",
                "id",
                "phases",
                "capabilities",
                "policies",
            }.issubset(profile_schema["required"])
        )
        self.assertTrue(
            {
                "schema",
                "id",
                "locator",
                "version",
                "inputs",
                "outputs",
                "permissions",
                "verified",
            }.issubset(capability_schema["required"])
        )

    def test_task_plan_and_run_bind_to_goal_revision(self):
        plan_schema = load_json(SCHEMAS / "task-plan-v1.schema.json")
        run_schema = load_json(SCHEMAS / "run-v1.schema.json")
        start_schema = load_json(SCHEMAS / "run-start-v1.schema.json")
        finish_schema = load_json(SCHEMAS / "run-finish-v1.schema.json")

        self.assertTrue(
            {"goal_revision", "phase", "tasks"}.issubset(
                plan_schema["required"]
            )
        )
        self.assertTrue(
            {
                "run_id",
                "role",
                "goal_revision",
                "phase",
                "task_id",
                "assignment_hash",
                "worker",
                "started_at",
                "outcome",
                "artifact_refs",
                "evidence_refs",
            }.issubset(run_schema["required"])
        )
        self.assertEqual(
            run_schema["properties"]["role"]["enum"],
            ["execution", "validation"],
        )
        self.assertTrue(
            {
                "candidate_hash",
                "criteria_hash",
                "input_hashes",
                "validation_fingerprint",
                "review_kind",
                "validation_conclusion",
            }.issubset(run_schema["properties"])
        )
        self.assertEqual(
            start_schema["$id"], "ideal-agent-loop/run-start-v1"
        )
        self.assertEqual(
            finish_schema["$id"], "ideal-agent-loop/run-finish-v1"
        )
        for record_schema in (start_schema, finish_schema):
            self.assertTrue(
                set(record_schema["required"]).issubset(
                    record_schema["properties"]
                )
            )
            self.assertFalse(record_schema["additionalProperties"])

    def test_development_and_document_share_the_same_profile_shape(self):
        development = load_json(DEVELOPMENT_PROFILE)
        document = load_json(DOCUMENT_PROFILE)

        for profile in (development, document):
            self.assertEqual(
                profile["schema"], "ideal-agent-loop/profile-v1"
            )
            self.assertTrue(profile["phases"])
            self.assertTrue(profile["capabilities"])
            self.assertIn("retry", profile["policies"])
            self.assertIn("review", profile["policies"])
            self.assertIn("permissions", profile["policies"])
            for phase in profile["phases"]:
                self.assertTrue(
                    {"id", "planner", "requires", "gate", "tasks"}
                    .issubset(phase)
                )

        self.assertEqual(
            development["adapters"],
            {
                "workspace": "git-worktree-optional",
                "integration_gate": "merge-gate",
            },
        )
        self.assertNotIn("adapters", document)

    def test_kernel_schemas_have_no_domain_specific_required_fields(self):
        schema_text = "\n".join(
            path.read_text(encoding="utf-8").lower()
            for path in sorted(SCHEMAS.glob("*.json"))
        )

        for forbidden in (
            "paper",
            "patent",
            "venue",
            "experiment",
            "worktree",
            "merge_gate",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, schema_text)


if __name__ == "__main__":
    unittest.main()
