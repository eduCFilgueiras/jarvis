# Architecture

Jarvis is a modular personal assistant prototype written in Python.

## Runtime Flow

```text
main.py
  -> src/interfaces/cli.py
      -> src/interfaces/commands.py
      -> src/core/jarvis.py
          -> src/core/orchestrator.py
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
- `security`: contains permission policy primitives.

## Agents

- `general`: handles conversational fallback, history intents, and tool intents.
- `dev`: placeholder development agent.

The development agent now creates a five-step plan from the project context and
requests authorization before any future write executor is added.

After authorization, `DevExecutor` currently produces a dry-run preview only;
it does not invoke shell commands or modify files.

`DevExecutionGuard` limits future execution to `inspect`, `test`, and `report`,
validates paths inside the project, and currently keeps external execution
disabled.

Controlled file writes use `FilesTool` after an explicit permission decision;
the DEV executor never invokes a shell.

Agents receive an `AgentContext` containing:

- `tools`
- `history`
- `model_provider`
- `permissions`

## Tools

Current tools:

- `calculator`
- `datetime`
- `files`
- `notes`
- `todo`

Tools are registered in `ToolRegistry` with a handler, description, and risk level,
and remain invokable by name for backwards compatibility.

## Security

`PermissionPolicy` provides the permission layer for tools.

Current behavior:

- read-only actions are auto-allowed by default.
- read-only actions are `ALLOW` by default.
- write actions return `ASK` and can be approved once through the CLI.
- destructive actions return `DENY`.
- all state-changing built-in tools are checked through the policy before execution.
- `files` supports controlled writes using `escrever arquivo caminho: conteudo`;
  writes require confirmation and remain restricted to the configured root.

## Models

Current providers:

- `mock`: default test/local provider.
- `openai`: optional provider requiring `OPENAI_API_KEY` and the `openai` extra.

The active model can be changed at runtime with `/model <name>`.

`ModelRegistry` can also route a destination such as `general` or `dev` to a
specific provider, while retaining the active provider as the fallback.

## Memory

The active CLI session keeps an in-memory conversation history.

Persistent memory is stored separately in `data/memory.json` and supports
`preference`, `fact`, and `project` categories with simple search.

General responses include at most five local memory items as context when
available; the complete memory store is never sent to a model request.

History can also be saved and loaded through:

- `/salvar`
- `/carregar`

## Voice

`VoicePipeline` separates speech-to-text, Jarvis message processing, and
text-to-speech. The current adapters are mocks for testing; real audio
providers can be added without changing the orchestrator.

Optional OpenAI STT/TTS adapters are available, but remain inactive unless
selected in configuration and provided with `OPENAI_API_KEY`.

`VoiceSession` models `IDLE`, `LISTENING`, `SPEAKING`, and `INTERRUPTED`
states so a future audio adapter can implement barge-in without coupling it
to Jarvis core.

`VoiceRuntime.run_once()` connects real audio devices to OpenAI STT/TTS for a
single controlled turn. Continuous listening remains opt-in and is not started
by the CLI automatically.

`ContinuousVoiceLoop` provides explicit continuous mode with a configurable
turn limit and stop phrases (`sair`, `parar`, `encerrar`).

`AudioInput` and `AudioOutput` isolate device access. Mock devices are used by
default in tests; `MacAudioInput` and `MacAudioOutput` use optional
`sounddevice`/`numpy` adapters when installed.

The default history path is `data/history.json`.

## Environments

`main.py` loads `.env` before creating the runtime `Jarvis` instance.

Supported reference files:

- `.env.example`
- `.env.hml.example`
- `.env.prd.example`
