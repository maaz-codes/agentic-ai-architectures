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
