import unittest

from src.security import PermissionPolicy, PermissionRequest


class PermissionPolicyTests(unittest.TestCase):
    def test_allows_read_only_actions_by_default(self) -> None:
        policy = PermissionPolicy()
        request = PermissionRequest(
            tool_name="files",
            action="read",
            resource="README.md",
        )

        decision = policy.check(request)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "read-only action allowed")

    def test_denies_read_only_actions_when_auto_allow_is_disabled(self) -> None:
        policy = PermissionPolicy(auto_allow_read_only=False)
        request = PermissionRequest(
            tool_name="files",
            action="read",
            resource="README.md",
        )

        decision = policy.check(request)

        self.assertFalse(decision.allowed)
        self.assertEqual(
            decision.reason,
            "Permissao necessaria para files.read em README.md.",
        )

    def test_denies_non_read_only_actions(self) -> None:
        policy = PermissionPolicy()
        request = PermissionRequest(
            tool_name="files",
            action="write",
            resource="README.md",
        )

        decision = policy.check(request)

        self.assertFalse(decision.allowed)
