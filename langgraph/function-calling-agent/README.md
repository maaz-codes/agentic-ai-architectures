# Function-Calling Agent (LangGraph)

> A LangGraph agent that uses OpenAI function calling to query real-time data (weather) and perform arithmetic, looping until no more tool calls remain.

## Architecture

```
User Query (MessagesState)
    │
    ▼
┌─────────────────┐
│  agent_reason   │  ← GPT-4o-mini with bound tools
│  (LLM node)     │
└────────┬────────┘
         │
    tool_calls?
         │
    ┌────┴────┐
   yes        no
    │          │
    ▼          ▼
tool_node     END
(ToolNode)
    │
    └──► back to agent_reason
```

## Key Concepts
- `MessagesState` as the graph's state schema — messages accumulate automatically
- `ToolNode` from LangGraph handles tool dispatch and result injection
- `should_continue` edge function checking for tool calls on the last message
- Graph visualization via `draw_mermaid_png`

## Tech Stack
- LangGraph · `langchain-openai` · OpenAI GPT-4o-mini

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd langgraph/function-calling-agent && uv sync`
3. `uv run python main.py`

## What I Learned
`MessagesState` + `ToolNode` together handle almost all the boilerplate of a tool-calling agent: message accumulation, tool routing, and result injection are automatic. The real work is in the `should_continue` conditional edge — it's the loop termination condition, and getting it wrong (e.g., checking the wrong message index) causes infinite loops or premature termination.
