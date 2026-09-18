import asyncio

from src.core.jarvis import jarvis, process_message
from src.interfaces import CliSession, run_cli


async def main() -> None:
    session = CliSession(
        agents=jarvis.agents,
        tools=jarvis.context.tools,
        history=jarvis.context.history,
        model_provider=jarvis.context.model_provider,
        config=jarvis.config,
    )
    await run_cli(process_message, session=session)


if __name__ == "__main__":
    asyncio.run(main())
