# Agentic AI Architectures

A collection of AI agent implementations exploring agentic patterns, RAG architectures, and LangGraph workflows. Built while studying the LangChain/LangGraph ecosystem — each project is a standalone implementation demonstrating a specific technique.

## Highlights

| Project | Category | What It Demonstrates |
|---------|----------|---------------------|
| [**Agentic RAG**](rag/agentic-rag/) | RAG | Adaptive retrieval with document grading, hallucination detection, and web search fallback |
| [**Reflexion Agent**](langgraph/reflexion-agent/) | LangGraph | Self-correcting agent with tool use, draft-revise loop, and iteration control |
| [**Hanoi Tower Solver**](langgraph/hanoi-tower-solver/) | LangGraph | LLM reasoning through constraint-satisfaction problems with error recovery |
| [**Async Ingestion Pipeline**](rag/async-ingestion-pipeline/) | RAG | Production-grade async document processing with concurrent batch uploads |
| [**ReAct From Scratch**](agents/react-from-scratch/) | Agents | Manual ReAct loop — no AgentExecutor, shows exactly what the framework abstracts away |
| [**Ice Breaker**](agents/ice-breaker/) | Agents | Full-stack agent pipeline: LinkedIn lookup → profile scraping → structured LLM analysis |

## Project Map

### `/agents` — Agent Patterns

| Project | Description |
|---------|-------------|
| [react-agent](agents/react-agent/) | Prebuilt ReAct agent with custom schema and prompt |
| [react-from-scratch](agents/react-from-scratch/) | Manual ReAct loop with explicit scratchpad management |
| [router-agent](agents/router-agent/) | Multi-agent router dispatching to code interpreter and CSV analyst |
| [ice-breaker](agents/ice-breaker/) | Two-stage pipeline: URL lookup agent → scraping → LLM profile analysis |

### `/rag` — Retrieval-Augmented Generation

| Project | Description |
|---------|-------------|
| [basic-rag](rag/basic-rag/) | Classic RAG with Pinecone and text ingestion |
| [inmemory-rag](rag/inmemory-rag/) | RAG with FAISS — no external vector DB |
| [async-ingestion-pipeline](rag/async-ingestion-pipeline/) | Async batch ingestion from Tavily crawl to Pinecone |
| [multimodal-rag](rag/multimodal-rag/) | Multi-modal pipeline: text + tables + images via Unstructured |
| [agentic-rag](rag/agentic-rag/) | CRAG: document grading, hallucination detection, web search fallback |

### `/langgraph` — LangGraph Workflows

| Project | Description |
|---------|-------------|
| [function-calling-agent](langgraph/function-calling-agent/) | Tool-calling agent with MessagesState and ToolNode |
| [reflection-agent](langgraph/reflection-agent/) | Generate → critique → revise loop with dual-persona chains |
| [reflexion-agent](langgraph/reflexion-agent/) | Reflexion paper: tool-augmented drafting with iterative revision |
| [hanoi-tower-solver](langgraph/hanoi-tower-solver/) | Constraint-satisfaction with LLM move generation and validation |

### `/multimodal` — Multimodal AI

| Project | Description |
|---------|-------------|
| [image-generation](multimodal/image-generation/) | Text-to-image and image-to-image transfer with Gemini 2.0 Flash |

## Tech Stack

Python 3.13 · LangChain 0.3 · LangGraph · OpenAI GPT-4o/mini · Google Gemini 2.0 · Pinecone · FAISS · ChromaDB · Tavily · Unstructured · Pydantic · uv

## Setup

Each project is standalone with its own `pyproject.toml`. From any project directory:

```bash
cp ../../.env.example .env   # fill in the keys you need
uv sync
uv run python main.py
```

See [`.env.example`](.env.example) for all required API keys.

## About

Built by [Maaz Khan](https://www.linkedin.com/in/maaz-khan-dev/). I'm an AI Agents Engineer specializing in agentic systems, RAG pipelines, and voice AI. Currently seeking remote opportunities.
