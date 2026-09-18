from src.agents import AgentContext, AgentRegistry, create_default_agent_registry
from src.core.config import JarvisConfig
from src.memory import ConversationHistory
from src.models import ModelProvider, create_default_model_registry
from src.router.router import route
from src.tools import ToolRegistry, create_default_tool_registry


class Jarvis:
    def __init__(
        self,
        agents: AgentRegistry | None = None,
        tools: ToolRegistry | None = None,
        history: ConversationHistory | None = None,
        model_provider: ModelProvider | None = None,
        config: JarvisConfig | None = None,
    ) -> None:
        self.agents = agents or create_default_agent_registry()
        self.config = config or JarvisConfig()
        self.context = AgentContext(
            tools=tools or create_default_tool_registry(),
            history=history or ConversationHistory(),
            model_provider=model_provider or create_default_model_registry(),
        )

    async def process_message(self, message: str) -> str:
        self.context.history.add_user_message(message)
        destination = route(message)

        if self.config.debug:
            print(f"Rota escolhida: {destination}")

        agent = self.agents.get(destination)
        response = await agent.execute(message, self.context)
        self.context.history.add_assistant_message(response)
        return response


jarvis = Jarvis()


async def process_message(message: str) -> str:
    return await jarvis.process_message(message)
