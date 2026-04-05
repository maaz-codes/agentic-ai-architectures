# Async Ingestion Pipeline

> Production-grade async document ingestion: crawl a documentation site with Tavily, chunk the pages, and batch-upload to Pinecone asynchronously with error handling per batch.

## Architecture

```
TavilyCrawl (https://python.langchain.com/)
    │  max_depth=1, extract_depth="advanced"
    ▼
List[Document] (raw_content + source URL)
    │
    ▼
RecursiveCharacterTextSplitter (4000 tokens, 200 overlap)
    │
    ▼
Batches of 500 chunks
    │
    ▼
asyncio.gather(*[vectorstore.aadd_documents(batch) for batch in batches])
    │  concurrent uploads, per-batch error handling
    ▼
Pinecone VectorStore
```

## Key Concepts
- `asyncio.gather` for concurrent batch uploads — dramatically faster than sequential
- Per-batch `try/except` so a single failed batch doesn't abort the entire pipeline
- SSL cert configuration with `certifi` for macOS compatibility
- `TavilyCrawl` for structured documentation scraping

## Tech Stack
- LangChain 0.3 · `langchain-pinecone` · `langchain-tavily` · `langchain-openai` · asyncio · certifi · Pinecone

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `TAVILY_API_KEY`
2. `cd rag/async-ingestion-pipeline && uv sync`
3. `uv run python ingestion.py`

## What I Learned
Async batch ingestion with `aadd_documents` is the right pattern for large document sets — a synchronous loop over 500+ Pinecone upserts hits rate limits and takes 10x longer. The key non-obvious detail: `asyncio.gather` with `return_exceptions=True` lets you collect failures without canceling successful concurrent tasks, making the pipeline resilient to partial outages.
