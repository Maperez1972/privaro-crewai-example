# Privaro + CrewAI Example

A runnable example showing how to use **Privaro** as a privacy layer for a simple CrewAI workflow before sending data to OpenAI.

## What this demo shows

1. Start with raw input that contains PII
2. Protect the input with Privaro
3. Run a CrewAI agent on sanitized data
4. Optionally reveal the final output through Privaro

## Files

- `app.py`
- `.env.example`
- `requirements.txt`

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Run

```bash
python app.py
```

## Architecture

```text
User Input -> Privaro Protect -> CrewAI Agent -> OpenAI -> Privaro Reveal
```

## Notes

This is intentionally minimal. You can expand it to multiple agents, tasks, and tools once the basic flow is validated.
