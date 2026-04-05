# Reflexion Agent

> LangGraph implementation of the Reflexion paper: an agent that uses tool-augmented research, self-reflection, and iterative revision to improve answers through multiple drafts.

## Architecture

```
Research Question
    │
    ▼
┌─────────────────────────────────────────┐
│              Reflexion Loop             │
│                                         │
│  first_responder  ──► Execute Tools     │
│  (draft + tool calls)   │               │
│                         ▼               │
│               tool_executor.py          │
│               (Tavily search)           │
│                         │               │
│                         ▼               │
│               revisor (reflect +        │
│               revise answer,            │
│               cite sources)             │
│                         │               │
│              ┌──────────┴────────┐      │
│         iterations < MAX     MAX reached│
│              │                   │      │
│              ▼                   ▼      │
│         first_responder         END     │
└─────────────────────────────────────────┘
```

## Key Concepts
- Reflexion paper pattern: draft → tool use → reflect → revise, repeat N times
- Pydantic schemas (`schemas.py`) for structured draft/revision output
- `tool_executor.py` wrapping Tavily search for grounded research
- Iteration control via `MAX_ITERATIONS` constant in graph

## Tech Stack
- LangGraph · `langchain-openai` · `langchain-tavily` · OpenAI GPT-4o-mini · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `TAVILY_API_KEY`
2. `cd langgraph/reflexion-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The key difference from a simple reflection loop is that Reflexion uses *tool-augmented* revision — the agent searches for new information to ground its self-critique, not just stylistic feedback. This means iterations actually converge on better answers rather than just more polished prose. Pydantic schemas for the draft/revision output make it easy to extract structured citations from the revision step.
