# ReAct Agent

> Demonstrates LangChain's prebuilt ReAct agent executor with OpenAI tool calling.

## Architecture

```
User Query
    │
    ▼
┌──────────────────────┐
│  create_react_agent  │  ← ReAct prompt from LangChain hub
│  (GPT-4o-mini)       │
└──────────┬───────────┘
           │ tool_call?
    ┌──────┴──────┐
    │             │
    ▼             ▼
 Execute        Final
  Tool         Answer
    │
    └──► back to agent
```

## Key Concepts
- ReAct (Reason + Act) prompting pattern
- LangChain `AgentExecutor` managing the tool-call loop
- Tool schema definition with Pydantic (`schemas.py`)
- Custom prompt injection via `prompt.py`

## Tech Stack
- LangChain 0.3 · `langchain-openai` · OpenAI GPT-4o-mini · `python-dotenv`

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd agents/react-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The prebuilt `create_react_agent` hides a surprising amount of complexity — the prompt template, output parser, and loop management are all wired together. Separating the schema (`schemas.py`) and prompt (`prompt.py`) from the main entrypoint makes the agent's "personality" easy to swap without touching orchestration logic.
