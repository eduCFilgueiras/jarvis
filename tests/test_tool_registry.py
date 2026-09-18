import unittest

from src.tools.registry import ToolRegistry, create_default_tool_registry


async def echo_tool(message: str) -> str:
    return message


class ToolRegistryTests(unittest.TestCase):
    def test_registers_and_lists_tools(self) -> None:
        registry = ToolRegistry()

        registry.register("echo", echo_tool)

        self.assertEqual(registry.names(), ["echo"])
        self.assertIs(registry.get("echo"), echo_tool)

    def test_unknown_tool_returns_none(self) -> None:
        registry = ToolRegistry()

        self.assertIsNone(registry.get("missing"))

    def test_default_registry_contains_datetime_tool(self) -> None:
        registry = create_default_tool_registry()

        self.assertEqual(
            registry.names(),
            ["calculator", "datetime", "files", "notes", "todo"],
        )
        self.assertIsNotNone(registry.get("calculator"))
        self.assertIsNotNone(registry.get("datetime"))
        self.assertIsNotNone(registry.get("files"))
        self.assertIsNotNone(registry.get("notes"))
        self.assertIsNotNone(registry.get("todo"))
