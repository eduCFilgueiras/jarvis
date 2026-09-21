import unittest

from src.agents.dev_executor import DevExecutor
from src.agents.dev_planner import DevPlanner


class DevExecutorTests(unittest.TestCase):
    def test_prepares_dry_run_without_side_effects(self) -> None:
        plan = DevPlanner().create_plan("corrigir bug")

        preview = DevExecutor().prepare(plan)

        self.assertTrue(preview.dry_run)
        self.assertEqual(len(preview.operations), 4)
        self.assertIn("Nenhum arquivo ou comando foi alterado", preview.render())
