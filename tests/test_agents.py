import unittest
from datetime import datetime

from src.agents.base import AgentContext
from src.agents.dev import DevAgent
from src.agents.dev_planner import DevPlanner
from src.agents.general import GeneralAgent
from src.memory import ConversationHistory
from src.models import MockModelProvider
from src.security import PermissionPolicy
from src.tools import CalculatorTool, DateTimeTool, FilesTool, TodoTool, ToolRegistry


def create_context(
    tools: ToolRegistry | None = None,
    history: ConversationHistory | None = None,
    permissions: PermissionPolicy | None = None,
) -> AgentContext:
    return AgentContext(
        tools=tools or ToolRegistry(),
        history=history or ConversationHistory(),
        model_provider=MockModelProvider(),
        permissions=permissions or PermissionPolicy(),
    )


class AgentTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.context = create_context()

    async def test_dev_agent_response(self) -> None:
        response = await DevAgent().execute("corrigir bug", self.context)

        self.assertIn('[DEV] Tarefa: "corrigir bug"', response)
        self.assertIn("Autorizacao necessaria", response)

    def test_dev_planner_creates_five_step_plan(self) -> None:
        plan = DevPlanner().create_plan("corrigir bug")

        self.assertEqual(len(plan.steps), 5)
        self.assertTrue(plan.authorization_required)

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
        context = create_context(tools=tools)

        response = await GeneralAgent().execute("que horas sao?", context)

        self.assertEqual(response, "Agora sao 14:30.")

    async def test_general_agent_uses_calculator_tool(self) -> None:
        tools = ToolRegistry()
        tool = CalculatorTool()
        tools.register("calculator", tool.execute)
        context = create_context(tools=tools)

        response = await GeneralAgent().execute("calcule 2 + 2", context)

        self.assertEqual(response, "O resultado e 4.")

    async def test_general_agent_returns_tool_errors_as_messages(self) -> None:
        tools = ToolRegistry()
        tool = TodoTool()
        tools.register("todo", tool.execute)
        context = create_context(tools=tools)

        response = await GeneralAgent().execute("criar tarefa", context)

        self.assertIn("Permissao negada: Permissao necessaria para todo.write", response)

    async def test_general_agent_summarizes_previous_user_messages(self) -> None:
        history = ConversationHistory()
        history.add_user_message("bom dia")
        history.add_assistant_message('[MODELO MOCK] Recebi: "bom dia"')
        history.add_user_message("calcule 2 + 2")
        history.add_assistant_message("O resultado e 4.")
        history.add_user_message("o que eu perguntei antes?")
        context = create_context(history=history)

        response = await GeneralAgent().execute("o que eu perguntei antes?", context)

        self.assertEqual(response, "Voce perguntou antes: bom dia; calcule 2 + 2.")

    async def test_general_agent_denies_files_when_policy_requires_permission(self) -> None:
        tools = ToolRegistry()
        tool = FilesTool()
        tools.register("files", tool.execute)
        context = create_context(
            tools=tools,
            permissions=PermissionPolicy(auto_allow_read_only=False),
        )

        response = await GeneralAgent().execute("listar arquivos", context)

        self.assertEqual(
            response,
            "Permissao negada: Permissao necessaria para files.list em listar arquivos.",
        )
