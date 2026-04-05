# In-Memory RAG

> RAG pipeline using FAISS for local, in-memory vector storage — no external vector DB required.

## Architecture

```
PDF file
    │
    ▼
PyPDFLoader
    │
    ▼
CharacterTextSplitter
    │
    ▼
FAISS.from_documents()  ──► save_local("faiss_index_react")
    │
    ▼
FAISS.load_local()
    │
    ▼
create_retrieval_chain(retriever, stuff_documents_chain)
    │
    ▼
Answer
```

## Key Concepts
- FAISS as a drop-in local alternative to Pinecone — zero infra, serialize to disk
- `create_retrieval_chain` + `create_stuff_documents_chain` composing a full RAG chain from primitives
- Prompt pulled from LangChain Hub (`langchain-ai/retrieval-qa-chat`)

## Tech Stack
- LangChain 0.3 · `langchain-community` · FAISS · OpenAI Embeddings · LangChain Hub

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd rag/inmemory-rag && uv sync`
3. `uv run python main.py` (builds index and queries in one run)

## What I Learned
FAISS's `save_local` / `load_local` pattern makes it practical for small-scale RAG without any external dependencies. The `allow_dangerous_deserialization=True` flag required for loading is a reminder that pickle-based serialization has security implications — it's fine for local dev but never deserialize untrusted FAISS indexes.
