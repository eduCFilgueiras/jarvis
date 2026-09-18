import unittest
from datetime import datetime

from src.tools.datetime_tool import DateTimeTool


class DateTimeToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_current_time(self) -> None:
        tool = DateTimeTool(clock=lambda: datetime(2026, 9, 18, 14, 30))

        response = await tool.execute("que horas sao?")

        self.assertEqual(response, "Agora sao 14:30.")

    async def test_returns_current_date(self) -> None:
        tool = DateTimeTool(clock=lambda: datetime(2026, 9, 18, 14, 30))

        response = await tool.execute("qual a data de hoje?")

        self.assertEqual(response, "Hoje e 18/09/2026.")
