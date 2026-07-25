import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "v1-backlog.md"


class MarkdownMirrorTests(unittest.TestCase):
    def test_render_is_deterministic_and_verifiable(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ideal_backlog.migrate_v1(
                root,
                FIXTURE,
                apply=True,
                operation_id="render-migration",
            )
            mirror = root / "docs" / "dev" / "需求池.md"

            first = ideal_backlog.render_current(root, mirror)
            second = ideal_backlog.render_current(root, mirror)

            self.assertEqual(first, second)
            self.assertIn("GENERATED MIRROR", first)
            self.assertIn("legacy_accepted", first)
            verification = ideal_backlog.verify_mirror(root, mirror)
            self.assertTrue(verification["matches"])

    def test_manually_edited_controlled_markdown_fails_verification(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ideal_backlog.migrate_v1(
                root,
                FIXTURE,
                apply=True,
                operation_id="edited-migration",
            )
            mirror = root / "需求池.md"
            ideal_backlog.render_current(root, mirror)
            mirror.write_text(
                mirror.read_text(encoding="utf-8") + "\nmanual edit\n",
                encoding="utf-8",
            )

            with self.assertRaises(ideal_backlog.MirrorMismatch):
                ideal_backlog.verify_mirror(root, mirror)


if __name__ == "__main__":
    unittest.main()
