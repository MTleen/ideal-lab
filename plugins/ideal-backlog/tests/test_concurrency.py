import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ideal_backlog  # noqa: E402


ONE_GOAL_FIXTURE = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "one-goal-backlog.json"
)


def initialize_one_goal(root):
    initial = ideal_backlog.init_store(root)
    snapshot = json.loads(ONE_GOAL_FIXTURE.read_text(encoding="utf-8"))
    return ideal_backlog.write_revision(
        root,
        snapshot,
        expected_revision=initial["revision"],
        operation_id="seed-one-goal",
    )


class LockAndLeaseTests(unittest.TestCase):
    def test_global_lock_is_exclusive_and_has_no_automatic_ttl(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ideal_backlog.init_store(root)

            token = ideal_backlog.acquire_lock(root, "writer-a", "lock-a")
            with self.assertRaises(ideal_backlog.LockConflict):
                ideal_backlog.acquire_lock(root, "writer-b", "lock-b")
            with self.assertRaises(ideal_backlog.LockConflict):
                ideal_backlog.acquire_lock(
                    root,
                    "writer-b",
                    "lock-b",
                    now="2999-01-01T00:00:00Z",
                )

            with self.assertRaises(ideal_backlog.LockConflict):
                ideal_backlog.release_lock(root, "wrong-token")
            ideal_backlog.release_lock(root, token)
            self.assertFalse(
                (root / ".ideal" / "backlog" / "LOCK").exists()
            )

    def test_claim_sets_a_lease_and_wrong_lease_cannot_transition(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seeded = initialize_one_goal(root)

            claimed = ideal_backlog.claim_goal(
                root,
                "REQ-001",
                expected_revision=seeded["revision"],
                operation_id="claim-1",
            )
            lease_token = claimed["snapshot"]["goals"][0]["lease"]["token"]

            self.assertTrue(lease_token)
            self.assertEqual(
                claimed["snapshot"]["goals"][0]["execution"]["status"],
                "claimed",
            )
            with self.assertRaises(ideal_backlog.LeaseConflict):
                ideal_backlog.transition_goal(
                    root,
                    "REQ-001",
                    expected_revision=claimed["revision"],
                    lease_token="wrong-lease",
                    operation_id="transition-wrong-lease",
                    patch={"execution": {"status": "planning"}},
                )

    def test_release_requires_the_goal_lease_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            seeded = initialize_one_goal(root)
            claimed = ideal_backlog.claim_goal(
                root,
                "REQ-001",
                expected_revision=seeded["revision"],
                operation_id="claim-2",
            )
            lease_token = claimed["snapshot"]["goals"][0]["lease"]["token"]

            with self.assertRaises(ideal_backlog.LeaseConflict):
                ideal_backlog.release_goal(
                    root,
                    "REQ-001",
                    expected_revision=claimed["revision"],
                    lease_token="wrong-lease",
                    operation_id="release-wrong",
                )
            released = ideal_backlog.release_goal(
                root,
                "REQ-001",
                expected_revision=claimed["revision"],
                lease_token=lease_token,
                operation_id="release-right",
            )
            replay = ideal_backlog.release_goal(
                root,
                "REQ-001",
                expected_revision=released["revision"],
                lease_token=lease_token,
                operation_id="release-right",
            )

            self.assertIsNone(released["snapshot"]["goals"][0]["lease"])
            self.assertEqual(replay["revision"], released["revision"])
            self.assertTrue(replay["replayed"])


if __name__ == "__main__":
    unittest.main()
