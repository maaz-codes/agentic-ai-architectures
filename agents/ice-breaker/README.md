# Ice Breaker

> Full-stack agent pipeline: given a person's name, look up their LinkedIn URL, scrape their profile, and generate a structured summary and conversation starters.

## Architecture

```
Person Name (input)
    │
    ▼
linkedin_lookup agent (GPT-4o-mini + Tavily search)
    │  returns LinkedIn profile URL
    ▼
Scrapin API  ──► raw LinkedIn JSON
    │
    ▼
LLM Chain (GPT-4o-mini)
    │  structured output via output_parser.py
    ▼
PersonInfo { summary, facts, topics, ice_breakers }
```

## Key Concepts
- Two-stage pipeline: URL discovery → data enrichment
- Tavily search as a tool for LinkedIn URL lookup
- `OutputFixingParser` wrapping a `PydanticOutputParser` for resilient JSON parsing
- Scrapin API for LinkedIn data without direct scraping

## Tech Stack
- LangChain 0.3 · `langchain-openai` · OpenAI GPT-4o-mini · Tavily · Scrapin API · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `TAVILY_API_KEY`, `SCRAPIN_API_KEY`
2. `cd agents/ice-breaker && uv sync`
3. `uv run python main.py`

## What I Learned
Chaining a search agent with a scraping API creates a surprisingly robust profile enrichment pipeline. The critical insight is separating concerns: the agent only finds the URL (a reasoning task), while a deterministic API call handles the actual data retrieval. Mixing them into one agent step makes the system fragile and harder to debug when LinkedIn blocks requests.
