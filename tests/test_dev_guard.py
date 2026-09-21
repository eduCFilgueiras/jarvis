import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.agents.dev_executor import AllowedOperation, DevExecutionGuard


class DevExecutionGuardTests(unittest.TestCase):
    def test_allows_safe_operation_inside_project(self) -> None:
        with TemporaryDirectory() as directory:
            guard = DevExecutionGuard(Path(directory))

            result = guard.execute(AllowedOperation.INSPECT, Path("src"))

        self.assertIn("validada", result)

    def test_blocks_path_outside_project(self) -> None:
        with TemporaryDirectory() as directory:
            guard = DevExecutionGuard(Path(directory))

            result = guard.execute(AllowedOperation.INSPECT, Path("../secret"))

        self.assertIn("bloqueada", result)
