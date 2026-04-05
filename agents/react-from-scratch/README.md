# ReAct Agent From Scratch

> Manual ReAct loop implementation — no AgentExecutor, no framework abstractions.

## Architecture

```
User Query
    │
    ▼
PromptTemplate (ReAct format)
    │
    ▼
GPT-4o-mini  ──stop=["\nObservation:"]──►  raw text
    │
    ▼
ReActSingleInputOutputParser
    │
    ├── AgentAction  ──► get_tool_by_name() ──► execute ──► observation
    │        │                                                    │
    │        └────────────── intermediate_steps ◄────────────────┘
    │
    └── AgentFinish  ──► return_values["output"]
```

## Key Concepts
- Manually formatting the ReAct scratchpad with `format_log_to_str`
- Using LLM `stop` tokens to halt generation at `Observation:`
- `ReActSingleInputOutputParser` parsing Thought/Action/Action Input
- No `AgentExecutor` — the while loop is written explicitly

## Tech Stack
- LangChain 0.3 · `langchain-openai` · OpenAI GPT-4o-mini

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd agents/react-from-scratch && uv sync`
3. `uv run python main.py`

## What I Learned
Building the ReAct loop manually reveals what `AgentExecutor` does under the hood: it's essentially a while loop that appends `(AgentAction, observation)` tuples to the scratchpad and re-invokes the LLM. The `stop` token trick is key — without it the LLM hallucinates its own observations instead of waiting for real tool output.
