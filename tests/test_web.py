import unittest

from src.interfaces.web import ControlState


class WebControlTests(unittest.TestCase):
    def test_state_snapshot_contains_observability_fields(self) -> None:
        state = ControlState()
        state.update("processing", "teste")
        snapshot = state.snapshot()

        self.assertEqual(snapshot["status"], "processing")
        self.assertEqual(snapshot["events"], ["teste"])
        self.assertIn("transcript", snapshot)
        self.assertIn("response", snapshot)
