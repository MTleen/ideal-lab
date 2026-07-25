import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


FIXTURE = (
    Path(__file__).resolve().parent / "fixtures" / "empty-backlog.json"
)


def empty_snapshot():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class RevisionStoreTests(unittest.TestCase):
    def test_init_store_creates_a_content_addressed_current_revision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            state = ideal_backlog.init_store(root)

            store = root / ".ideal" / "backlog"
            current = (store / "CURRENT").read_text(encoding="utf-8").strip()
            revision_file = store / "revisions" / current / "backlog.json"
            persisted = json.loads(revision_file.read_text(encoding="utf-8"))
            self.assertEqual(state["revision"], current)
            self.assertEqual(current, ideal_backlog.revision_hash(persisted))

    def test_read_current_rejects_content_that_does_not_match_current(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            state = ideal_backlog.init_store(root)
            revision_file = (
                root
                / ".ideal"
                / "backlog"
                / "revisions"
                / state["revision"]
                / "backlog.json"
            )
            revision_file.write_text('{"tampered":true}\n', encoding="utf-8")

            with self.assertRaises(ideal_backlog.IntegrityError):
                ideal_backlog.read_current(root)

    def test_write_revision_rejects_a_stale_expected_revision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ideal_backlog.init_store(root)

            with self.assertRaises(ideal_backlog.StaleRevision):
                ideal_backlog.write_revision(
                    root,
                    empty_snapshot(),
                    expected_revision="not-current",
                    operation_id="op-stale",
                )

    def test_repeated_operation_returns_its_original_revision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initial = ideal_backlog.init_store(root)
            first_snapshot = empty_snapshot()
            first_snapshot["metadata"]["label"] = "first"
            first = ideal_backlog.write_revision(
                root,
                first_snapshot,
                expected_revision=initial["revision"],
                operation_id="op-first",
            )
            second_snapshot = copy.deepcopy(first["snapshot"])
            second_snapshot["metadata"]["label"] = "second"
            second = ideal_backlog.write_revision(
                root,
                second_snapshot,
                expected_revision=first["revision"],
                operation_id="op-second",
            )

            replay = ideal_backlog.write_revision(
                root,
                first_snapshot,
                expected_revision=initial["revision"],
                operation_id="op-first",
            )

            self.assertEqual(replay["revision"], first["revision"])
            self.assertTrue(replay["replayed"])
            self.assertEqual(
                ideal_backlog.read_current(root)["revision"],
                second["revision"],
            )

    def test_reused_operation_id_rejects_a_different_request(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initial = ideal_backlog.init_store(root)
            snapshot = empty_snapshot()
            snapshot["metadata"]["label"] = "first"
            first = ideal_backlog.write_revision(
                root,
                snapshot,
                expected_revision=initial["revision"],
                operation_id="op-shared",
            )
            conflicting = copy.deepcopy(snapshot)
            conflicting["metadata"]["label"] = "different"

            with self.assertRaises(ideal_backlog.IdempotencyConflict):
                ideal_backlog.write_revision(
                    root,
                    conflicting,
                    expected_revision=first["revision"],
                    operation_id="op-shared",
                )

    def test_current_reads_inject_the_observed_store_revision(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initial = ideal_backlog.init_store(root)
            snapshot = empty_snapshot()
            snapshot["goals"] = [
                {
                    "id": "OBSERVED",
                    "revision": "",
                }
            ]
            written = ideal_backlog.write_revision(
                root,
                snapshot,
                expected_revision=initial["revision"],
                operation_id="observe-write",
            )

            current = ideal_backlog.read_current(root)

            self.assertEqual(current["revision"], written["revision"])
            self.assertEqual(
                current["snapshot"]["goals"][0]["revision"],
                current["revision"],
            )

    def test_later_writes_never_modify_existing_revision_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            initial = ideal_backlog.init_store(root)
            first_file = (
                root
                / ".ideal"
                / "backlog"
                / "revisions"
                / initial["revision"]
                / "backlog.json"
            )
            original_bytes = first_file.read_bytes()
            snapshot = copy.deepcopy(initial["snapshot"])
            snapshot["metadata"]["label"] = "next"

            ideal_backlog.write_revision(
                root,
                snapshot,
                expected_revision=initial["revision"],
                operation_id="op-next",
            )

            self.assertEqual(first_file.read_bytes(), original_bytes)


if __name__ == "__main__":
    unittest.main()
