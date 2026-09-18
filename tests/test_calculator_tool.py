import unittest

from src.tools.calculator_tool import CalculatorTool


class CalculatorToolTests(unittest.IsolatedAsyncioTestCase):
    async def test_adds_numbers(self) -> None:
        response = await CalculatorTool().execute("calcule 2 + 2")

        self.assertEqual(response, "O resultado e 4.")

    async def test_respects_precedence(self) -> None:
        response = await CalculatorTool().execute("quanto e 2 + 3 * 4")

        self.assertEqual(response, "O resultado e 14.")

    async def test_handles_decimal_numbers(self) -> None:
        response = await CalculatorTool().execute("calcule 10 / 4")

        self.assertEqual(response, "O resultado e 2.5.")

    async def test_rejects_non_math_expression(self) -> None:
        with self.assertRaises(ValueError):
            await CalculatorTool().execute("calcule algo")
