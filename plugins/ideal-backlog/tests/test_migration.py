import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class MigrationTests(unittest.TestCase):
    def test_dry_run_is_non_mutating_and_reports_the_mapped_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = FIXTURES / "v1-backlog.md"

            report = ideal_backlog.migrate_v1(
                root, source, apply=False
            )

            self.assertTrue(report["can_apply"])
            self.assertFalse((root / ".ideal" / "backlog").exists())
            self.assertEqual(len(report["snapshot"]["goals"]), 2)
            self.assertEqual(
                report["source_sha256"],
                hashlib.sha256(source.read_bytes()).hexdigest(),
            )

    def test_apply_preserves_v1_fields_and_archives_the_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = FIXTURES / "v1-backlog.md"

            result = ideal_backlog.migrate_v1(
                root,
                source,
                apply=True,
                operation_id="migrate-v1-test",
            )
            current = ideal_backlog.read_current(root)
            first, historical = current["snapshot"]["goals"]
            migration = current["snapshot"]["metadata"]["migration"]

            self.assertEqual(result["revision"], current["revision"])
            self.assertEqual(first["priority"], "P0")
            self.assertEqual(first["created_at"], "2026-07-01")
            self.assertEqual(first["dependencies"], ["REQ-000"])
            self.assertEqual(first["execution"]["status"], "executing")
            self.assertEqual(first["quality"]["status"], "implemented")
            self.assertEqual(
                first["quality"]["evidence"],
                ["自动验证：tests/store.log"],
            )
            self.assertEqual(
                first["reopen_history"][0]["required_regression"],
                "cover stale expected revisions",
            )
            self.assertEqual(
                historical["quality"]["status"], "legacy_accepted"
            )
            self.assertTrue(historical["quality"]["legacy"])
            self.assertEqual(
                migration["source_sha256"],
                hashlib.sha256(source.read_bytes()).hexdigest(),
            )
            archived = (
                root
                / migration["source_snapshot_ref"]
            )
            self.assertEqual(archived.read_bytes(), source.read_bytes())

    def test_unknown_controlled_fields_block_apply_without_creating_a_store(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            with self.assertRaises(ideal_backlog.MigrationError) as raised:
                ideal_backlog.migrate_v1(
                    root,
                    FIXTURES / "v1-backlog-edge-cases.md",
                    apply=True,
                    operation_id="migrate-edge",
                )

            self.assertIn("神秘状态", str(raised.exception))
            self.assertFalse((root / ".ideal" / "backlog").exists())


if __name__ == "__main__":
    unittest.main()
