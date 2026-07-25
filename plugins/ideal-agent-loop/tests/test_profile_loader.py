import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


PLUGIN_ROOT = Path(__file__).resolve().parents[1]


class ProfileLoaderTests(unittest.TestCase):
    def test_loads_both_public_profile_shapes(self):
        development = loop_kernel.load_profile(
            PLUGIN_ROOT / "profiles" / "development.json"
        )
        document = loop_kernel.load_profile(
            Path(__file__).resolve().parent
            / "fixtures"
            / "document-profile.json"
        )

        self.assertEqual(development["id"], "development")
        self.assertEqual(document["id"], "document")

    def test_rejects_a_profile_without_required_policy_contracts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            path.write_text(
                json.dumps(
                    {
                        "schema": "ideal-agent-loop/profile-v1",
                        "id": "invalid",
                        "phases": [],
                        "capabilities": {},
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaises(loop_kernel.ContractError):
                loop_kernel.load_profile(path)

    def test_load_capabilities_preserves_locator_and_version(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "capabilities.json"
            path.write_text(
                json.dumps(
                    {
                        "capabilities": [
                            {
                                "schema": "ideal-agent-loop/capability-v1",
                                "id": "compose",
                                "locator": "example:compose",
                                "version": "2.3.4",
                                "inputs": ["assignment"],
                                "outputs": ["artifact"],
                                "permissions": ["workspace-read"],
                                "verified": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            capabilities = loop_kernel.load_capabilities(path)

            self.assertEqual(capabilities[0]["locator"], "example:compose")
            self.assertEqual(capabilities[0]["version"], "2.3.4")


if __name__ == "__main__":
    unittest.main()
