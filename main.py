import asyncio

from src.core.env import load_env
from src.interfaces import CliSession, run_cli

load_env()

from src.core.jarvis import jarvis, process_message  # noqa: E402


async def main() -> None:
    session = CliSession(
        agents=jarvis.agents,
        tools=jarvis.context.tools,
        history=jarvis.context.history,
        model_provider=jarvis.context.model_provider,
        config=jarvis.config,
        permissions=jarvis.context.permissions,
        memory=jarvis.context.memory,
    )
    await run_cli(process_message, session=session)


if __name__ == "__main__":
    asyncio.run(main())
