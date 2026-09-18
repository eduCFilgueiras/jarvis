import unittest
from datetime import datetime

from src.agents.base import AgentContext
from src.agents.dev import DevAgent
from src.agents.general import GeneralAgent
from src.memory import ConversationHistory
from src.models import MockModelProvider
from src.tools import CalculatorTool, DateTimeTool, TodoTool, ToolRegistry


class AgentTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.context = AgentContext(
            tools=ToolRegistry(),
            history=ConversationHistory(),
            model_provider=MockModelProvider(),
        )

    async def test_dev_agent_response(self) -> None:
        response = await DevAgent().execute("corrigir bug", self.context)

        self.assertEqual(response, '[DEV] Recebi a tarefa: "corrigir bug"')

    async def test_general_agent_response(self) -> None:
        response = await GeneralAgent().execute("bom dia", self.context)

        self.assertEqual(response, '[MODELO MOCK] Recebi: "bom dia"')

    async def test_general_agent_does_not_treat_greeting_as_date_request(self) -> None:
        response = await GeneralAgent().execute("bom dia", self.context)

        self.assertEqual(response, '[MODELO MOCK] Recebi: "bom dia"')

    async def test_general_agent_uses_datetime_tool(self) -> None:
        tools = ToolRegistry()
        tool = DateTimeTool(clock=lambda: datetime(2026, 9, 18, 14, 30))
        tools.register("datetime", tool.execute)
        context = AgentContext(
            tools=tools,
            history=ConversationHistory(),
            model_provider=MockModelProvider(),
        )

        response = await GeneralAgent().execute("que horas sao?", context)

        self.assertEqual(response, "Agora sao 14:30.")

    async def test_general_agent_uses_calculator_tool(self) -> None:
        tools = ToolRegistry()
        tool = CalculatorTool()
        tools.register("calculator", tool.execute)
        context = AgentContext(
            tools=tools,
            history=ConversationHistory(),
            model_provider=MockModelProvider(),
        )

        response = await GeneralAgent().execute("calcule 2 + 2", context)

        self.assertEqual(response, "O resultado e 4.")

    async def test_general_agent_returns_tool_errors_as_messages(self) -> None:
        tools = ToolRegistry()
        tool = TodoTool()
        tools.register("todo", tool.execute)
        context = AgentContext(
            tools=tools,
            history=ConversationHistory(),
            model_provider=MockModelProvider(),
        )

        response = await GeneralAgent().execute("criar tarefa", context)

        self.assertEqual(response, "Erro na ferramenta todo: Nenhuma tarefa informada.")

    async def test_general_agent_summarizes_previous_user_messages(self) -> None:
        history = ConversationHistory()
        history.add_user_message("bom dia")
        history.add_assistant_message('[MODELO MOCK] Recebi: "bom dia"')
        history.add_user_message("calcule 2 + 2")
        history.add_assistant_message("O resultado e 4.")
        history.add_user_message("o que eu perguntei antes?")
        context = AgentContext(
            tools=ToolRegistry(),
            history=history,
            model_provider=MockModelProvider(),
        )

        response = await GeneralAgent().execute("o que eu perguntei antes?", context)

        self.assertEqual(response, "Voce perguntou antes: bom dia; calcule 2 + 2.")
