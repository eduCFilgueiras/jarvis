import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents.dev_executor import DevExecutionGuard
from src.security import PermissionPolicy


class DevWriteTests(unittest.IsolatedAsyncioTestCase):
    async def test_write_requires_permission_then_writes(self) -> None:
        with TemporaryDirectory() as directory:
            guard = DevExecutionGuard(Path(directory))
            permissions = PermissionPolicy(auto_allow_read_only=False)
            response = await guard.write_file(Path("change.txt"), "ok", permissions)
            self.assertIn("Permissao pendente", response)
            permissions.grant_pending()
            response = await guard.write_file(Path("change.txt"), "ok", permissions)
            self.assertIn("Arquivo escrito", response)
            self.assertEqual((Path(directory) / "change.txt").read_text(), "ok")
