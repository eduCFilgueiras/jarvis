# Environments

Jarvis supports environment-specific configuration through environment variables.

The CLI loads `.env` automatically when `main.py` starts. Existing OS
environment variables are not overwritten.

## Files

- `.env.example`: local/default reference.
- `.env.hml.example`: homologation reference.
- `.env.prd.example`: production reference.

Real files are ignored by Git:

- `.env`
- `.env.local`
- `.env.hml`
- `.env.prd`

## Variables

- `JARVIS_ENV`: `local`, `hml`, or `prd`.
- `JARVIS_LANGUAGE`: interface language, currently `pt-BR`.
- `JARVIS_DEBUG`: `true` or `false`.
- `JARVIS_TIMEZONE`: timezone label.
- `JARVIS_HISTORY_LIMIT`: number used by future memory limits.
- `JARVIS_HISTORY_PATH`: JSON history persistence path.
- `JARVIS_EXPORT_PATH`: Markdown export path.
- `OPENAI_API_KEY`: optional key for the OpenAI provider.

## Suggested Usage

Local:

```bash
cp .env.example .env
python3 main.py
```

HML:

```bash
cp .env.hml.example .env
python3 main.py
```

PRD:

```bash
cp .env.prd.example .env
python3 main.py
```

For production-like usage, keep `JARVIS_DEBUG=false`.
