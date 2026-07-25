import importlib.util
import json
import sys
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


def load_script(name):
    path = SCRIPTS_DIR / (name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


agent_loop_state = load_script("agent_loop_state")
agent_loop_verify = load_script("agent_loop_verify")


class DevelopmentProfileCompatibilityTests(unittest.TestCase):
    def test_workspace_adapter_is_optional_and_profile_owned(self):
        development = loop_kernel.load_profile(
            PLUGIN_ROOT / "profiles" / "development.json"
        )
        document = loop_kernel.load_profile(
            Path(__file__).resolve().parent
            / "fixtures"
            / "document-profile.json"
        )

        dev_adapters = loop_kernel.adapters_for_phase(
            development, "implementation"
        )
        document_adapters = loop_kernel.adapters_for_phase(document, "draft")

        self.assertEqual(
            dev_adapters["workspace"]["id"], "git-worktree-optional"
        )
        self.assertTrue(dev_adapters["workspace"]["optional"])
        self.assertIsNone(document_adapters["workspace"])

    def test_integration_gate_only_activates_in_its_configured_phase(self):
        development = loop_kernel.load_profile(
            PLUGIN_ROOT / "profiles" / "development.json"
        )

        requirement = loop_kernel.adapters_for_phase(
            development, "requirement"
        )
        implementation = loop_kernel.adapters_for_phase(
            development, "implementation"
        )

        self.assertIsNone(requirement["integration_gate"])
        self.assertEqual(
            implementation["integration_gate"]["id"], "merge-gate"
        )

    def test_legacy_criteria_import_as_required_evidence_artifacts(self):
        contract = {
            "criteria": [
                {
                    "id": 1,
                    "desc": "Focused checks pass",
                    "verify_type": "script",
                    "command": "python3 -m unittest",
                    "affected_files": ["src/example.py"],
                }
            ]
        }

        imported = agent_loop_state.import_legacy_criteria(contract)

        self.assertEqual(
            imported["required_artifacts"][0]["id"],
            "criterion-1-evidence",
        )
        self.assertEqual(
            imported["required_artifacts"][0]["role"], "validation"
        )
        self.assertTrue(imported["criteria_hash"].startswith("sha256:"))

    def test_legacy_verifier_projects_evidence_not_candidate_artifacts(self):
        projected = agent_loop_verify.project_validation_result(
            {
                "criterion_id": 1,
                "status": "passed",
                "evidence": "tests passed",
            }
        )

        self.assertEqual(projected["role"], "validation")
        self.assertEqual(projected["artifact_refs"], [])
        self.assertEqual(
            projected["evidence_refs"], ["criterion://1/tests-passed"]
        )

    def test_kernel_has_no_hardcoded_development_worker_locator(self):
        source = (
            SCRIPTS_DIR / "loop_kernel.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("ideal-dev-workflow", source)


if __name__ == "__main__":
    unittest.main()
