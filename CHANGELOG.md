# Changelog

## 0.1.0

Initial Python version of Jarvis.

Added:

- Python CLI loop.
- Modular architecture with `core`, `router`, `agents`, `tools`, `models`, `memory`, and `interfaces`.
- Agent registry with `general` and `dev` agents.
- Tool registry.
- Tools: calculator, datetime, files, notes, todo.
- Intent router for history and tool calls.
- In-session memory.
- JSON save/load for conversation history.
- Markdown session export.
- Model provider abstraction.
- Mock model provider.
- Optional OpenAI model provider.
- Model registry and runtime model switching.
- CLI commands for help, history, status, config, version, diagnostics, model switching, debug, save/load, and export.
- Permission policy primitives for tool safety.
- Optional OpenAI dependency group in `pyproject.toml`.
- `.env.example`.
- Unit test suite.
