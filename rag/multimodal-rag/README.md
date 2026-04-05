# Multimodal RAG

> Multi-modal document understanding pipeline: partition a PDF into text, tables, and images; summarize each modality; store in ChromaDB; retrieve and answer with GPT-4o.

## Architecture

```
PDF Document
    │
    ▼
Unstructured (partition_pdf)
    │
    ├── Text elements
    ├── Table elements  ──► HTML representation
    └── Image elements  ──► base64
            │
            ▼
    Summarize each chunk (GPT-4o-mini)
            │
            ▼
    ChromaDB (summary embeddings + original content in metadata)
            │
            ▼
    Retriever (k=3, similarity)
            │
            ▼
    GPT-4o (text + embedded images in message)
            │
            ▼
         Answer
```

## Key Concepts
- `partition_pdf` from `unstructured` for modality-aware document parsing
- Storing original multimodal content in metadata while embedding only the summary
- Multi-vector retrieval: embedding summaries, returning originals
- Injecting base64 images directly into GPT-4o message content

## Tech Stack
- LangChain 0.3 · `unstructured` · `langchain-openai` · ChromaDB · GPT-4o · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. Install system dependencies: `brew install poppler tesseract` (for PDF/image parsing)
3. `cd rag/multimodal-rag && uv sync` (or `pip install -r ingestion-pipeline/requirements.txt`)
4. Place your PDF at `docs/attention-is-all-you-need.pdf`
5. Run ingestion: `uv run python ingestion-pipeline/multi-modal-rag.py`
6. Run retrieval: `uv run python mRAG.py`

## What I Learned
The critical insight is that you cannot embed images directly — you embed a text summary of the image but retrieve the original for the LLM. This multi-vector pattern generalizes to any content type where the embedding index and the retrieved payload need to differ. `unstructured`'s ability to extract table HTML (not just raw text) preserves the relational structure that pure text extraction destroys.
