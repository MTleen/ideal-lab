import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "v1-backlog.md"


class BacklogCliTests(unittest.TestCase):
    def run_cli(self, arguments):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = ideal_backlog.main(arguments)
        return exit_code, json.loads(output.getvalue())

    def test_migration_dry_run_and_apply_are_explicit_and_auditable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            dry_code, dry_report = self.run_cli(
                [
                    "--root",
                    str(root),
                    "migrate-v1",
                    "--source",
                    str(FIXTURE),
                    "--dry-run",
                ]
            )

            self.assertEqual(dry_code, 0)
            self.assertTrue(dry_report["can_apply"])
            self.assertFalse((root / ".ideal").exists())

            apply_code, applied = self.run_cli(
                [
                    "--root",
                    str(root),
                    "migrate-v1",
                    "--source",
                    str(FIXTURE),
                    "--apply",
                    "--operation-id",
                    "cli-migrate",
                ]
            )
            verify_code, verified = self.run_cli(
                ["--root", str(root), "verify"]
            )

            self.assertEqual(apply_code, 0)
            self.assertTrue(applied["revision"])
            self.assertEqual(verify_code, 0)
            self.assertTrue(verified["valid"])

    def test_write_commands_require_apply(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    ideal_backlog.main(
                        ["--root", temp_dir, "init"]
                    )

    def test_cli_declares_every_v2_command(self):
        parser = ideal_backlog.build_parser()
        command_action = next(
            action
            for action in parser._actions
            if getattr(action, "dest", None) == "command"
        )

        self.assertEqual(
            set(command_action.choices),
            {
                "init",
                "inspect",
                "migrate-v1",
                "render",
                "verify",
                "verify-mirror",
                "claim",
                "transition",
                "release",
                "accept",
                "restore",
                "reopen",
            },
        )


if __name__ == "__main__":
    unittest.main()
