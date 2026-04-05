# Agentic RAG (CRAG)

> Corrective RAG with a LangGraph state machine: routes queries, grades retrieved documents for relevance, detects hallucinations, and falls back to web search when retrieval is insufficient.

## Architecture

```
User Query
    │
    ▼
Question Router (GPT-4o-mini + structured output)
    │
    ├── "vectorstore" ──► Retrieve from Pinecone
    │                          │
    │                    Grade Documents (per doc: relevant? yes/no)
    │                          │
    │              ┌───────────┴───────────┐
    │         all relevant            any irrelevant
    │              │                       │
    │              ▼                       ▼
    │           Generate             Web Search (Tavily)
    │              │                       │
    │        Hallucination Check           │
    │        (grounded in docs?)           │
    │              │                       │
    │         ┌────┴────┐                  │
    │    grounded   hallucinated           │
    │         │         │                  │
    │         ▼         ▼                  │
    │       Answer   Web Search ───────────┘
    │                                  │
    └── "websearch" ───────────────────┤
                                       ▼
                                   Generate
                                       │
                                       ▼
                                    Answer
```

## Key Concepts
- LangGraph `StateGraph` orchestrating multi-step conditional retrieval
- Document grading with `with_structured_output(GradeDocuments)` — binary yes/no relevance
- Hallucination detection as a separate chain after generation
- Adaptive routing: vectorstore vs. web search decided per query

## Tech Stack
- LangGraph · LangChain 0.3 · `langchain-openai` · OpenAI GPT-4o-mini · Pinecone · Tavily · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `TAVILY_API_KEY`
2. `cd rag/agentic-rag && uv sync`
3. `uv run python graph/graph.py`

## What I Learned
The hallucination grader is the most architecturally interesting piece. Checking generation quality after the fact (rather than just retrieving better) creates a self-correcting loop that dramatically reduces confident wrong answers. The non-obvious design decision: the hallucination check gates on whether the answer is grounded in the *retrieved documents*, not whether it's factually correct — this is cheaper to evaluate and sufficient for the use case.
