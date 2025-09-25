from typing import Any, Dict

from graph.state import GraphState
from ingestion_pinecone import retriver


def retrieve(state: GraphState) -> Dict:
    print("---RETRIEVE---")

    question = state["question"]
    documents = retriver.invoke(question)

    return {"documents": documents}