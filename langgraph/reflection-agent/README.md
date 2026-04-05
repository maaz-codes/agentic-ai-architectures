# Reflection Agent

> LangGraph agent that iteratively improves its output through a generate-reflect loop: generates a response, then critiques it, then generates again.

## Architecture

```
Initial Prompt (HumanMessage)
    │
    ▼
┌──────────┐
│ generate │  ← generation_chain (writer persona)
└────┬─────┘
     │
 len(messages) > 2?
     │
┌────┴────┐
no        yes
│          │
▼          ▼
reflect   END
│
▼
┌──────────┐
│ reflect  │  ← reflection_chain (critic persona), output as HumanMessage
└──────────┘
     │
     └──► back to generate
```

## Key Concepts
- Reflection as a separate chain with a critic system prompt
- Reflection output injected back as `HumanMessage` so the generator sees it as "user feedback"
- Iteration bounded by message count (not a separate counter)
- Two chains (`generation_chain`, `reflection_chain`) with distinct personas

## Tech Stack
- LangGraph · `langchain-openai` · OpenAI GPT-4o-mini

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd langgraph/reflection-agent && uv sync`
3. `uv run python main.py`

## What I Learned
Injecting the reflection as a `HumanMessage` rather than a special message type is an elegant trick — it reuses the LLM's existing instruction-following behavior ("user said to improve X") without needing to fine-tune or prompt-engineer a new format. The limitation is that the LLM can't distinguish "original user request" from "reflection feedback" in the message history, which matters for multi-turn applications.
