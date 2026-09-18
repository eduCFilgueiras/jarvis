# Architecture

Jarvis is a modular personal assistant prototype written in Python.

## Runtime Flow

```text
main.py
  -> src/interfaces/cli.py
      -> src/interfaces/commands.py
      -> src/core/jarvis.py
          -> src/router/router.py
          -> src/agents/registry.py
          -> src/agents/general.py or src/agents/dev.py
              -> src/router/intent_router.py
              -> src/tools/registry.py
              -> src/models/registry.py
              -> src/memory/conversation_history.py
```

## Modules

- `core`: owns `Jarvis`, runtime config, and orchestration.
- `interfaces`: owns the CLI loop and internal slash commands.
- `router`: routes messages to agents and routes general-agent intents.
- `agents`: contains agent contracts and concrete agents.
- `tools`: contains local deterministic capabilities.
- `models`: contains the model-provider abstraction and model registry.
- `memory`: contains in-session history and JSON persistence.

## Agents

- `general`: handles conversational fallback, history intents, and tool intents.
- `dev`: placeholder development agent.

Agents receive an `AgentContext` containing:

- `tools`
- `history`
- `model_provider`

## Tools

Current tools:

- `calculator`
- `datetime`
- `files`
- `notes`
- `todo`

Tools are registered in `ToolRegistry` and invoked by name.

## Models

Current providers:

- `mock`: default test/local provider.
- `openai`: optional provider requiring `OPENAI_API_KEY` and the `openai` extra.

The active model can be changed at runtime with `/model <name>`.

## Memory

The active CLI session keeps an in-memory conversation history.

History can also be saved and loaded through:

- `/salvar`
- `/carregar`

The default history path is `data/history.json`.
