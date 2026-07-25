import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import loop_kernel  # noqa: E402


REQUIREMENT = {
    "id": "compose",
    "inputs": ["assignment", "source"],
    "outputs": ["artifact"],
    "permissions": ["workspace-read"],
}


def candidate(
    locator,
    *,
    inputs=None,
    outputs=None,
    permissions=None,
    verified=True,
    preference=100,
):
    return {
        "schema": "ideal-agent-loop/capability-v1",
        "id": "compose",
        "locator": locator,
        "version": "1.2.3",
        "inputs": inputs or ["assignment", "source"],
        "outputs": outputs or ["artifact"],
        "permissions": (
            ["workspace-read"] if permissions is None else permissions
        ),
        "verified": verified,
        "preference": preference,
    }


class CapabilityResolverTests(unittest.TestCase):
    def test_selects_exact_contract_match_by_deterministic_preference(self):
        selected = loop_kernel.resolve_capability(
            REQUIREMENT,
            [
                candidate("worker:later", preference=20),
                candidate("worker:first", preference=10),
            ],
            allowed_permissions=["workspace-read"],
        )

        self.assertEqual(selected["locator"], "worker:first")
        self.assertEqual(selected["version"], "1.2.3")

    def test_excludes_contract_permission_and_verification_mismatches(self):
        selected = loop_kernel.resolve_capability(
            REQUIREMENT,
            [
                candidate("worker:wrong-input", inputs=["assignment"]),
                candidate(
                    "worker:denied",
                    permissions=["workspace-read", "network"],
                ),
                candidate("worker:unverified", verified=False),
                candidate("worker:valid"),
            ],
            allowed_permissions=["workspace-read"],
        )

        self.assertEqual(selected["locator"], "worker:valid")

    def test_permissions_must_exactly_match_the_task_requirement(self):
        result = loop_kernel.resolve_capability(
            REQUIREMENT,
            [
                candidate("worker:missing", permissions=[]),
                candidate(
                    "worker:expanded",
                    permissions=["workspace-read", "workspace-write"],
                ),
            ],
            allowed_permissions=["workspace-read", "workspace-write"],
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["reason"], "capability_unavailable")

    def test_missing_capability_returns_a_structured_block(self):
        result = loop_kernel.resolve_capability(
            REQUIREMENT,
            [candidate("worker:guess", outputs=["different-artifact"])],
            allowed_permissions=["workspace-read"],
        )

        self.assertEqual(result["outcome"], "blocked")
        self.assertEqual(result["reason"], "capability_unavailable")
        self.assertEqual(result["required"], REQUIREMENT)


if __name__ == "__main__":
    unittest.main()
