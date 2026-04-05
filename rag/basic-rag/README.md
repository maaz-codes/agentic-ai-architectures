# Basic RAG

> Classic retrieval-augmented generation pipeline: ingest a text document into Pinecone, then query it with a RAG chain.

## Architecture

```
INGESTION                          RETRIEVAL
─────────                          ─────────
text file                          User Query
    │                                  │
    ▼                                  ▼
CharacterTextSplitter          OpenAI Embeddings
    │                                  │
    ▼                                  ▼
OpenAI Embeddings              Pinecone similarity search
    │                                  │
    ▼                                  ▼
Pinecone VectorStore           Retrieved docs + query
                                       │
                                       ▼
                               LLM (GPT-4o-mini)
                                       │
                                       ▼
                                    Answer
```

## Key Concepts
- Two-script pattern: `ingestion.py` (one-time) + `main.py` (query loop)
- Pinecone as persistent vector store
- `CharacterTextSplitter` with overlap to prevent context loss at chunk boundaries

## Tech Stack
- LangChain 0.3 · `langchain-pinecone` · `langchain-openai` · Pinecone · OpenAI Embeddings

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`
2. `cd rag/basic-rag && uv sync`
3. Run ingestion once: `uv run python ingestion.py`
4. Run queries: `uv run python main.py`

## What I Learned
The chunk size / overlap settings have a larger impact on answer quality than the retrieval `k` value. Too-large chunks retrieve irrelevant context that confuses the LLM; too-small chunks lose the sentence context needed for coherent answers. A 1000-token chunk with 200-token overlap works well for article-length documents.
