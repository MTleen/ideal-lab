import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


LOOP_PLUGIN = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = LOOP_PLUGIN / "scripts"
BACKLOG_PLUGIN = LOOP_PLUGIN.parent / "ideal-backlog"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(BACKLOG_PLUGIN / "scripts"))

import ideal_backlog  # noqa: E402
import loop_kernel  # noqa: E402


V1_FIXTURE = (
    BACKLOG_PLUGIN / "tests" / "fixtures" / "v1-backlog.md"
)


class KernelCliTests(unittest.TestCase):
    def test_step_reads_backlog_only_through_cli_and_emits_one_assignment(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            migrated = ideal_backlog.migrate_v1(
                root,
                V1_FIXTURE,
                apply=True,
                operation_id="kernel-cli-seed",
            )
            claimed = ideal_backlog.claim_goal(
                root,
                "REQ-001",
                migrated["revision"],
                "kernel-cli-claim",
            )
            lease_token = claimed["snapshot"]["goals"][0]["lease"][
                "token"
            ]
            capabilities_path = root / "capabilities.json"
            capabilities_path.write_text(
                json.dumps(
                    {
                        "capabilities": [
                            {
                                "schema": "ideal-agent-loop/capability-v1",
                                "id": "code-implementation",
                                "locator": "mock:implement",
                                "version": "1.0.0",
                                "inputs": [
                                    "task-assignment",
                                    "project-context",
                                ],
                                "outputs": [
                                    "implementation-artifact"
                                ],
                                "permissions": [
                                    "workspace-read",
                                    "workspace-write",
                                    "process-exec",
                                ],
                                "verified": True,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            output = io.StringIO()

            with contextlib.redirect_stdout(output):
                exit_code = loop_kernel.main(
                    [
                        "step",
                        "--backlog-cli",
                        str(BACKLOG_PLUGIN / "scripts" / "ideal_backlog.py"),
                        "--project-root",
                        str(root),
                        "--profile",
                        str(LOOP_PLUGIN / "profiles" / "development.json"),
                        "--capabilities",
                        str(capabilities_path),
                        "--source-binding",
                        "fixed",
                        "--goal-id",
                        "REQ-001",
                        "--lease-token",
                        lease_token,
                        "--apply",
                    ]
                )

            result = json.loads(output.getvalue())
            self.assertEqual(exit_code, 0)
            self.assertEqual(result["outcome"], "assignment")
            self.assertEqual(result["role"], "execution")
            self.assertEqual(
                result["assignment"]["capability"]["locator"],
                "mock:implement",
            )

    def test_step_requires_apply(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                loop_kernel.main(
                    [
                        "step",
                        "--backlog-cli",
                        "backlog.py",
                        "--project-root",
                        ".",
                        "--profile",
                        "profile.json",
                        "--capabilities",
                        "capabilities.json",
                        "--source-binding",
                        "dynamic",
                    ]
                )


if __name__ == "__main__":
    unittest.main()
