# Router Agent

> Multi-agent router that dispatches to specialized sub-agents: a Python code interpreter and a CSV data analyst.

## Architecture

```
User Request (natural language)
    │
    ▼
┌─────────────────────────────────┐
│  Tool-Calling Agent (GPT-4o)    │
└────────────┬────────────────────┘
             │ routes to
      ┌──────┴──────┐
      │             │
      ▼             ▼
python_agent    csv_agent
(code exec)   (pandas on
               seinfeld.csv)
```

## Key Concepts
- `create_tool_calling_agent` as the router (vs. `create_react_agent`)
- Sub-agents wrapped as `Tool` objects with descriptive docstrings that guide routing
- `create_csv_agent` for natural-language pandas queries
- `create_python_agent` for arbitrary code generation + execution

## Tech Stack
- LangChain 0.3 · `langchain-experimental` · OpenAI GPT-4o · LangChain Hub

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd agents/router-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The routing quality depends almost entirely on the tool description strings — the LLM has no other signal for which sub-agent to use. Saying "takes ONLY natural language requests" and "DO NOT pass Python code" in the description was necessary to stop the router from pre-generating code before handing off, which caused the code agent to re-execute already-generated code incorrectly.
