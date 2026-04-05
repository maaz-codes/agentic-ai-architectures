# Portfolio Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform `learn-langchain` from a numbered tutorial journal into a portfolio showcase repo named `agentic-ai-architectures`, grouped by technique with polished READMEs and secrets purged from history.

**Architecture:** Strip live API keys from git history entirely using git-filter-repo, delete noise projects, reorganize into `agents/`, `rag/`, `langgraph/`, `multimodal/` categories using `git mv` to preserve history, fix hardcoded paths, write per-project READMEs, and commit everything in one clean commit.

**Tech Stack:** git, git-filter-repo, Python 3.13, uv, LangChain 0.3, LangGraph, OpenAI, Google Gemini, Pinecone, FAISS, Tavily, Pydantic

---

## File Map

**Deleted:**
- `00-basics/` — entire directory
- `12.1-console_script/` — entire directory
- `servers/` — entire directory
- `main.py` (root)
- `langchain_client.py` (root)
- `pyproject.toml` (root)
- `uv.lock` (root)
- `.env` (root) — purged from all history
- `.DS_Store` files everywhere

**Created:**
- `.gitignore`
- `.env.example`
- `agents/react-agent/README.md`
- `agents/react-from-scratch/README.md`
- `agents/router-agent/README.md`
- `agents/ice-breaker/README.md`
- `rag/basic-rag/README.md`
- `rag/inmemory-rag/README.md`
- `rag/async-ingestion-pipeline/README.md`
- `rag/multimodal-rag/README.md`
- `rag/agentic-rag/README.md`
- `langgraph/function-calling-agent/README.md`
- `langgraph/reflection-agent/README.md`
- `langgraph/reflexion-agent/README.md`
- `langgraph/hanoi-tower-solver/README.md`
- `multimodal/image-generation/README.md`
- `README.md` (root, rewritten)

**Modified (hardcoded path fixes):**
- `rag/basic-rag/ingestion.py` — absolute path → `os.path.dirname(__file__)`
- `rag/inmemory-rag/main.py` — absolute path → `os.path.dirname(__file__)`
- `rag/multimodal-rag/ingestion-pipeline/multi-modal-rag.py` — absolute path → relative `"docs/attention-is-all-you-need.pdf"`
- `rag/multimodal-rag/mRAG.py` — absolute path → relative `"dbv2"`
- `multimodal/image-generation/image-gen.py` — absolute paths → `os.path.dirname(__file__)`
- `multimodal/image-generation/learning/image-1.py` — absolute path → `os.path.dirname(__file__)`
- `multimodal/image-generation/learning/image-3.py` — absolute path → `os.path.dirname(__file__)`

**Moved (git mv):**
- `01-react-agent` → `agents/react-agent`
- `02-deep-dive-react` → `agents/react-from-scratch`
- `05-router-agent` → `agents/router-agent`
- `06-ice-breaker` → `agents/ice-breaker`
- `03-intro-to-RAG/03.01-basic-RAG` → `rag/basic-rag`
- `03-intro-to-RAG/03.02-vectorstore-inmemory` → `rag/inmemory-rag`
- `04-langchain-helper-RAG` → `rag/async-ingestion-pipeline`
- `08-multi-rag` → `rag/multimodal-rag`
- `12-Agentic-RAG/graph` → `rag/agentic-rag`
- `09-langgraph` → `langgraph/function-calling-agent`
- `10-Refection-agent` → `langgraph/reflection-agent`
- `11-Reflexion-agent` → `langgraph/reflexion-agent`
- `13-Hanoi-Tower` → `langgraph/hanoi-tower-solver`
- `07-image-gen` → `multimodal/image-generation`

---

## Task 1: Install git-filter-repo and purge .env from history

**Files:**
- Create: `.gitignore`
- Delete from history: `.env`

- [ ] **Step 1: Install git-filter-repo**

```bash
pip install git-filter-repo
# verify:
git filter-repo --version
```

Expected output: version string like `2.38.0`

- [ ] **Step 2: Create .gitignore**

Create `/Users/maazkhan/Desktop/learn-langchain/.gitignore` with:

```
.env
.DS_Store
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/
faiss_index_react/
dbv1/
dbv2/
van-gogh-v2.png
*.png
!07-image-gen/images/*.png
!multimodal/image-generation/images/*.png
```

Wait — don't ignore all PNGs; the flow/graph PNGs in LangGraph projects and the sample images are worth keeping. Use a targeted rule instead:

```
.env
.DS_Store
**/.DS_Store
__pycache__/
*.pyc
*.pyo
.venv/
venv/
*.egg-info/
dist/
build/
faiss_index_react/
dbv1/
dbv2/
van-gogh-v2.png
maakhan-van-gogh-v1.png
```

- [ ] **Step 3: Delete .env from working tree**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
rm .env
```

- [ ] **Step 4: Purge .env from all git history**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git filter-repo --path .env --invert-paths --force
```

Expected: output listing rewritten commits, ending with something like `Ref 'refs/heads/main' was rewritten`

- [ ] **Step 5: Remove any .DS_Store files from git tracking**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
find . -name ".DS_Store" -not -path "./.git/*" -exec git rm --cached --ignore-unmatch {} \;
```

- [ ] **Step 6: Create .env.example**

Create `/Users/maazkhan/Desktop/learn-langchain/.env.example`:

```
# OpenAI — used by most agent and RAG projects
OPENAI_API_KEY=your-openai-api-key

# Google Gemini — used by multimodal/image-generation
GOOGLE_API_KEY=your-google-api-key

# LangSmith tracing (optional)
LANGSMITH_TRACING=false
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_PROJECT="agentic-ai-architectures"

# Tavily search — used by agentic-rag, async-ingestion-pipeline
TAVILY_API_KEY=your-tavily-api-key

# Pinecone vector DB — used by basic-rag, async-ingestion-pipeline, hanoi-tower-solver
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=agentic-rag

# Scrapin — used by agents/ice-breaker (LinkedIn profile scraping)
SCRAPIN_API_KEY=your-scrapin-api-key
```

---

## Task 2: Delete noise directories and root MCP files

**Files:**
- Delete: `00-basics/`, `12.1-console_script/`, `servers/`, `main.py`, `langchain_client.py`, `pyproject.toml`, `uv.lock`

- [ ] **Step 1: Remove tutorial and stub directories**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git rm -r 00-basics/
git rm -r 12.1-console_script/
git rm -r servers/
```

- [ ] **Step 2: Remove root MCP experiment files**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git rm main.py langchain_client.py pyproject.toml uv.lock
```

- [ ] **Step 3: Verify staging looks right**

```bash
git status --short | head -40
```

Expected: a long list of `D` (deleted) entries for the removed files.

---

## Task 3: Create category directories and move agents/ projects

**Files:** Uses `git mv` to move 4 project directories.

- [ ] **Step 1: Create category directories**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
mkdir -p agents rag langgraph multimodal
```

- [ ] **Step 2: Move agent projects**

```bash
git mv 01-react-agent agents/react-agent
git mv 02-deep-dive-react agents/react-from-scratch
git mv 05-router-agent agents/router-agent
git mv 06-ice-breaker agents/ice-breaker
```

- [ ] **Step 3: Verify**

```bash
ls agents/
```

Expected: `ice-breaker  react-agent  react-from-scratch  router-agent`

---

## Task 4: Move rag/ projects

**Files:** 5 moves; `03-intro-to-RAG` parent dir removed after both children are extracted.

- [ ] **Step 1: Move RAG projects**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git mv 03-intro-to-RAG/03.01-basic-RAG rag/basic-rag
git mv 03-intro-to-RAG/03.02-vectorstore-inmemory rag/inmemory-rag
git mv 04-langchain-helper-RAG rag/async-ingestion-pipeline
git mv 08-multi-rag rag/multimodal-rag
git mv 12-Agentic-RAG/graph rag/agentic-rag
```

- [ ] **Step 2: Remove now-empty parent directories**

```bash
git rm -r 03-intro-to-RAG
git rm -r 12-Agentic-RAG
```

Note: `12-Agentic-RAG/CRAG/` contains only a PNG diagram — not worth keeping as a standalone directory.

- [ ] **Step 3: Verify**

```bash
ls rag/
```

Expected: `agentic-rag  async-ingestion-pipeline  basic-rag  inmemory-rag  multimodal-rag`

---

## Task 5: Move langgraph/ projects

**Files:** 4 moves, including typo fix on reflection-agent.

- [ ] **Step 1: Move LangGraph projects**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git mv 09-langgraph langgraph/function-calling-agent
git mv 10-Refection-agent langgraph/reflection-agent
git mv 11-Reflexion-agent langgraph/reflexion-agent
git mv 13-Hanoi-Tower langgraph/hanoi-tower-solver
```

- [ ] **Step 2: Verify**

```bash
ls langgraph/
```

Expected: `function-calling-agent  hanoi-tower-solver  reflection-agent  reflexion-agent`

---

## Task 6: Move multimodal/ project

- [ ] **Step 1: Move image-generation**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git mv 07-image-gen multimodal/image-generation
```

- [ ] **Step 2: Verify**

```bash
ls multimodal/
```

Expected: `image-generation`

---

## Task 7: Fix hardcoded absolute paths in source files

After the moves, these files have hardcoded `/Users/maakhan/...` paths that will break on any other machine.

### 7a: rag/basic-rag/ingestion.py

- [ ] **Step 1: Fix TextLoader path**

In `rag/basic-rag/ingestion.py`, line 17 currently reads:
```python
    loader = TextLoader("/Users/maakhan/Desktop/langchain-course/03-intro-to-RAG/03.01-basic-RAG/vector-medium-blog-1.txt")
```

Change to:
```python
    loader = TextLoader(os.path.join(os.path.dirname(__file__), "vector-medium-blog-1.txt"))
```

Also add `import os` at the top (after the existing imports, before `from unittest import loader` — actually that import is `from unittest import loader` which is wrong but **do not change logic**, just add `import os`).

The file top already has `import os` — verify first with a quick read; if not present, add it after line 1.

### 7b: rag/inmemory-rag/main.py

- [ ] **Step 2: Fix PyPDFLoader path**

In `rag/inmemory-rag/main.py`, line 18:
```python
    pdf_path = "/Users/maakhan/Desktop/langchain-course/03-intro-to-RAG/03.02-vectorstore-inmemory/react-agent.pdf"
```

Change to:
```python
    pdf_path = os.path.join(os.path.dirname(__file__), "react-agent.pdf")
```

`import os` is already present at line 1.

### 7c: rag/multimodal-rag/ingestion-pipeline/multi-modal-rag.py

- [ ] **Step 3: Fix PDF path**

In `rag/multimodal-rag/ingestion-pipeline/multi-modal-rag.py`, line 43:
```python
    file_path = "/Users/maakhan/Desktop/langchain-course/docs/attention-is-all-you-need.pdf"
```

Change to:
```python
    file_path = "docs/attention-is-all-you-need.pdf"
```

(This PDF is not bundled in the repo — the relative path tells users where to place it.)

### 7d: rag/multimodal-rag/mRAG.py

- [ ] **Step 4: Fix ChromaDB persist path**

In `rag/multimodal-rag/mRAG.py`, line 102:
```python
    db = load_existing_vector_store(persist_directory="/Users/mac/Desktop/langchain-learn/dbv2")
```

Change to:
```python
    db = load_existing_vector_store(persist_directory="dbv2")
```

### 7e: multimodal/image-generation/image-gen.py

- [ ] **Step 5: Fix image paths in image-gen.py**

In `multimodal/image-generation/image-gen.py`, lines 72–73:
```python
    image1_path = "/Users/maakhan/Desktop/langchain-course/images/image_local.png"
    image2_path = "/Users/maakhan/Desktop/langchain-course/images/starry_night.jpg"
```

Change to:
```python
    image1_path = os.path.join(os.path.dirname(__file__), "images", "image_local.png")
    image2_path = os.path.join(os.path.dirname(__file__), "images", "starry_night.jpg")
```

Then add `import os` at the top of the file (it's not currently imported). Add it after the `import io` line.

### 7f: multimodal/image-generation/learning/image-1.py

- [ ] **Step 6: Fix image path in learning/image-1.py**

In `multimodal/image-generation/learning/image-1.py`, line 34:
```python
    image_file_path = "/Users/maakhan/Desktop/langchain-course/image_local.png"
```

Change to (file is inside `learning/`, images are in `../images/`):
```python
    image_file_path = os.path.join(os.path.dirname(__file__), "..", "images", "image_local.png")
```

`import os` is not in this file. Add it after `import base64` (line 2).

### 7g: multimodal/image-generation/learning/image-3.py

- [ ] **Step 7: Fix module-level image path in learning/image-3.py**

In `multimodal/image-generation/learning/image-3.py`, line 15 (module-level, not inside a function):
```python
image_file_path = "/Users/maakhan/Desktop/langchain-course/image_local.png"
```

Change to:
```python
image_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "image_local.png")
```

Add `import os` at the top (after existing imports).

---

## Task 8: Write agents/ READMEs

### 8a: agents/react-agent/README.md

- [ ] **Step 1: Write agents/react-agent/README.md**

```markdown
# ReAct Agent

> Demonstrates LangChain's prebuilt ReAct agent executor with OpenAI tool calling.

## Architecture

```
User Query
    │
    ▼
┌──────────────────────┐
│  create_react_agent  │  ← ReAct prompt from LangChain hub
│  (GPT-4o-mini)       │
└──────────┬───────────┘
           │ tool_call?
    ┌──────┴──────┐
    │             │
    ▼             ▼
 Execute        Final
  Tool         Answer
    │
    └──► back to agent
```

## Key Concepts
- ReAct (Reason + Act) prompting pattern
- LangChain `AgentExecutor` managing the tool-call loop
- Tool schema definition with Pydantic (`schemas.py`)
- Custom prompt injection via `prompt.py`

## Tech Stack
- LangChain 0.3 · `langchain-openai` · OpenAI GPT-4o-mini · `python-dotenv`

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd agents/react-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The prebuilt `create_react_agent` hides a surprising amount of complexity — the prompt template, output parser, and loop management are all wired together. Separating the schema (`schemas.py`) and prompt (`prompt.py`) from the main entrypoint makes the agent's "personality" easy to swap without touching orchestration logic.
```

### 8b: agents/react-from-scratch/README.md

- [ ] **Step 2: Write agents/react-from-scratch/README.md**

```markdown
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
```

### 8c: agents/router-agent/README.md

- [ ] **Step 3: Write agents/router-agent/README.md**

```markdown
# Router Agent

> Multi-agent router that dispatches to specialized sub-agents: a Python code interpreter and a CSV data analyst.

## Architecture

```
User Request (natural language)
    │
    ▼
┌─────────────────────────────────┐
│  Tool-Calling Agent (GPT-4o)    │
└────────────┬────────────────────┘
             │ routes to
      ┌──────┴──────┐
      │             │
      ▼             ▼
python_agent    csv_agent
(code exec)   (pandas on
               seinfeld.csv)
```

## Key Concepts
- `create_tool_calling_agent` as the router (vs. `create_react_agent`)
- Sub-agents wrapped as `Tool` objects with descriptive docstrings that guide routing
- `create_csv_agent` for natural-language pandas queries
- `create_python_agent` for arbitrary code generation + execution

## Tech Stack
- LangChain 0.3 · `langchain-experimental` · OpenAI GPT-4o · LangChain Hub

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`
2. `cd agents/router-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The routing quality depends almost entirely on the tool description strings — the LLM has no other signal for which sub-agent to use. Saying "takes ONLY natural language requests" and "DO NOT pass Python code" in the description was necessary to stop the router from pre-generating code before handing off, which caused the code agent to re-execute already-generated code incorrectly.
```

### 8d: agents/ice-breaker/README.md

- [ ] **Step 4: Write agents/ice-breaker/README.md**

```markdown
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
```

---

## Task 9: Write rag/ READMEs

### 9a: rag/basic-rag/README.md

- [ ] **Step 1: Write rag/basic-rag/README.md**

```markdown
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
```

### 9b: rag/inmemory-rag/README.md

- [ ] **Step 2: Write rag/inmemory-rag/README.md**

```markdown
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
```

### 9c: rag/async-ingestion-pipeline/README.md

- [ ] **Step 3: Write rag/async-ingestion-pipeline/README.md**

```markdown
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
```

### 9d: rag/multimodal-rag/README.md

- [ ] **Step 4: Write rag/multimodal-rag/README.md**

```markdown
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
```

### 9e: rag/agentic-rag/README.md

- [ ] **Step 5: Write rag/agentic-rag/README.md**

```markdown
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
2. `cd rag/agentic-rag && uv sync` (note: no `pyproject.toml` at this level — deps are defined in parent)
3. `uv run python graph/graph.py`

## What I Learned
The hallucination grader is the most architecturally interesting piece. Checking generation quality after the fact (rather than just retrieving better) creates a self-correcting loop that dramatically reduces confident wrong answers. The non-obvious design decision: the hallucination check gates on whether the answer is grounded in the *retrieved documents*, not whether it's factually correct — this is cheaper to evaluate and sufficient for the use case.
```

---

## Task 10: Write langgraph/ READMEs

### 10a: langgraph/function-calling-agent/README.md

- [ ] **Step 1: Write langgraph/function-calling-agent/README.md**

```markdown
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
```

### 10b: langgraph/reflection-agent/README.md

- [ ] **Step 2: Write langgraph/reflection-agent/README.md**

```markdown
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
```

### 10c: langgraph/reflexion-agent/README.md

- [ ] **Step 3: Write langgraph/reflexion-agent/README.md**

```markdown
# Reflexion Agent

> LangGraph implementation of the Reflexion paper: an agent that uses tool-augmented research, self-reflection, and iterative revision to improve answers through multiple drafts.

## Architecture

```
Research Question
    │
    ▼
┌─────────────────────────────────────────┐
│              Reflexion Loop             │
│                                         │
│  first_responder  ──► Execute Tools     │
│  (draft + tool calls)   │               │
│                         ▼               │
│               tool_executor.py          │
│               (Tavily search)           │
│                         │               │
│                         ▼               │
│               revisor (reflect +        │
│               revise answer,            │
│               cite sources)             │
│                         │               │
│              ┌──────────┴────────┐      │
│         iterations < MAX     MAX reached│
│              │                   │      │
│              ▼                   ▼      │
│         first_responder         END     │
└─────────────────────────────────────────┘
```

## Key Concepts
- Reflexion paper pattern: draft → tool use → reflect → revise, repeat N times
- Pydantic schemas (`schemas.py`) for structured draft/revision output
- `tool_executor.py` wrapping Tavily search for grounded research
- Iteration control via `MAX_ITERATIONS` constant in graph

## Tech Stack
- LangGraph · `langchain-openai` · `langchain-tavily` · OpenAI GPT-4o-mini · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `TAVILY_API_KEY`
2. `cd langgraph/reflexion-agent && uv sync`
3. `uv run python main.py`

## What I Learned
The key difference from a simple reflection loop is that Reflexion uses *tool-augmented* revision — the agent searches for new information to ground its self-critique, not just stylistic feedback. This means iterations actually converge on better answers rather than just more polished prose. Pydantic schemas for the draft/revision output make it easy to extract structured citations from the revision step.
```

### 10d: langgraph/hanoi-tower-solver/README.md

- [ ] **Step 4: Write langgraph/hanoi-tower-solver/README.md**

```markdown
# Hanoi Tower Solver

> LangGraph agent that solves the Tower of Hanoi through LLM reasoning, validating each move against physical constraints and recovering from invalid moves.

## Architecture

```
Initial State: n disks on peg A, goal: move all to peg C
    │
    ▼
┌─────────────────────────────────────────┐
│              Hanoi Graph                │
│                                         │
│  move_generator  ──► proposed move      │
│  (LLM reasons about current state)  │   │
│                      │                  │
│                      ▼                  │
│               move_validator            │
│               (constraint check:        │
│                no larger on smaller)    │
│                      │                  │
│              ┌───────┴───────┐          │
│           valid           invalid       │
│              │                │         │
│              ▼                ▼         │
│         apply_move      error_handler   │
│              │          (explain why)   │
│              │                │         │
│         solved?               │         │
│         ┌───┴───┐             │         │
│        yes      no            │         │
│         │       │             │         │
│         ▼       └─────────────┘         │
│        END       move_generator         │
└─────────────────────────────────────────┘
```

## Key Concepts
- LLM as a constraint-satisfaction solver with explicit state tracking
- Error recovery loop: invalid moves feed back with explanation to the LLM
- Pinecone used for storing game state history (see `ingestion_pinecone.py`)
- LangGraph's conditional edges for valid/invalid branching

## Tech Stack
- LangGraph · `langchain-openai` · `langchain-pinecone` · OpenAI GPT-4o-mini · Pinecone · Pydantic

## How to Run
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`, `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`
2. `cd langgraph/hanoi-tower-solver && uv sync`
3. `uv run python main.py`

## What I Learned
LLMs are surprisingly capable at Tower of Hanoi when given explicit state representation and constraint feedback — they don't need to reason from scratch each step if the current peg state is in the prompt. The error recovery loop was necessary: the LLM occasionally makes invalid moves (trying to place a larger disk on a smaller one), and rather than aborting, feeding back the specific constraint violation lets it self-correct within 1-2 retries.
```

---

## Task 11: Write multimodal/image-generation/README.md

- [ ] **Step 1: Write multimodal/image-generation/README.md**

```markdown
# Image Generation

> Gemini multimodal pipeline: text-to-image generation and image-to-image style transfer using Google's Gemini 2.0 Flash image generation model.

## Architecture

```
Text Prompt [+ optional input image]
    │
    ▼
ChatGoogleGenerativeAI
(gemini-2.0-flash-preview-image-generation)
response_modalities=["TEXT", "IMAGE"]
    │
    ├── text content  ──► print description
    └── image_url     ──► base64 decode ──► PIL.Image ──► save .png
```

## Key Concepts
- Gemini's `response_modalities=["TEXT", "IMAGE"]` to request multimodal output
- Extracting base64 image data from the `image_url` block in the response
- Image-to-image transfer: encoding input as base64 and passing in message content
- `learning/` subdirectory contains step-by-step progression scripts

## Tech Stack
- `langchain-google-genai` · Google Gemini 2.0 Flash · PIL (Pillow) · `python-dotenv`

## How to Run
1. Copy `.env.example` to `.env` and fill in `GOOGLE_API_KEY`
2. `cd multimodal/image-generation`
3. Install deps: `pip install langchain-google-genai pillow python-dotenv`
4. Run: `python image-gen.py`
5. Output saved as `van-gogh-v2.png` in current directory

## What I Learned
Gemini's image generation API is notably different from OpenAI's DALL-E: it returns image data inline in the chat message (as a base64 `image_url` block) rather than as a separate URL endpoint. The `response_modalities` parameter must be set in `generation_config`, not in the standard LangChain invoke kwargs — this is a Gemini-specific pattern that the LangChain wrapper exposes via a passthrough.
```

---

## Task 12: Write root README.md

- [ ] **Step 1: Write README.md at repo root**

```markdown
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
```

---

## Task 13: Update git remote URL

- [ ] **Step 1: Update origin to new repo name**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git remote set-url origin git@github.com:maaz-codes/agentic-ai-architectures.git
```

- [ ] **Step 2: Verify**

```bash
git remote -v
```

Expected:
```
origin  git@github.com:maaz-codes/agentic-ai-architectures.git (fetch)
origin  git@github.com:maaz-codes/agentic-ai-architectures.git (push)
```

---

## Task 14: Stage everything and make the single commit

- [ ] **Step 1: Stage all changes**

```bash
cd /Users/maazkhan/Desktop/learn-langchain
git add -A
```

- [ ] **Step 2: Review what's staged**

```bash
git status --short | wc -l
git status --short | grep "^D" | wc -l
git status --short | grep "^R" | wc -l
git status --short | grep "^A" | wc -l
```

Expected: many deleted (D), many renamed (R), new files (A). Should see no modifications to .env (it's deleted and purged).

- [ ] **Step 3: Commit**

```bash
git commit -m "$(cat <<'EOF'
Restructure as portfolio showcase — group by technique, add READMEs, strip secrets

- Purge .env (live API keys) from all git history via git-filter-repo
- Add .gitignore and .env.example
- Delete 00-basics, 12.1-console_script, servers, root MCP files
- Reorganize into agents/, rag/, langgraph/, multimodal/ by technique
- Fix hardcoded /Users/maakhan/... paths in 7 source files
- Add README.md to all 14 projects and root
- Update git remote to maaz-codes/agentic-ai-architectures

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 4: Verify commit**

```bash
git log --oneline -3
git show --stat HEAD | tail -20
```

Expected: commit at top showing many file renames and additions.

---

## Self-Review

### Spec Coverage Check

| Requirement | Task |
|-------------|------|
| .env purged from history | Task 1 |
| .gitignore created | Task 1 |
| .env deleted from working tree | Task 1 |
| .env.example with all keys | Task 1 |
| Rename remote to agentic-ai-architectures | Task 13 |
| Remove 00-basics/ | Task 2 |
| Remove 12.1-console_script/ | Task 2 |
| Remove servers/ + root main.py + langchain_client.py | Task 2 |
| agents/ with 4 projects (git mv) | Task 3 |
| rag/ with 5 projects (git mv) | Task 4 |
| langgraph/ with 4 projects (git mv) | Task 5 |
| multimodal/ with 1 project (git mv) | Task 6 |
| Fix hardcoded paths in image-gen | Task 7 |
| Fix hardcoded paths in multimodal-rag | Task 7 |
| Fix hardcoded paths in basic-rag, inmemory-rag | Task 7 |
| Remove .DS_Store files | Task 1, Step 5 |
| Per-project READMEs (14 projects) | Tasks 8–11 |
| Root README.md with highlights table + project map | Task 12 |
| Single commit | Task 14 |

### Gaps / Notes
- `rag/agentic-rag` has no `pyproject.toml` of its own (was inside `12-Agentic-RAG/graph`). The project works standalone since it uses `load_dotenv()` but users will need to install deps manually. The README How to Run reflects this.
- `multimodal/image-generation` has no `pyproject.toml`. README instructs `pip install` instead.
- After `git filter-repo`, the git remote tracking may be reset — Task 13 explicitly sets the remote, covering this.
- The `12-Agentic-RAG/CRAG/` directory contains only `CRAG-graph.png` — deleted in Task 4 along with the empty parent. No code lost.
