from typing TypedDict, List
from graph.state import GraphState
from graph.chains.generation import generation_chain

def generate(state: GraphState) -> dict:
    print("---GENERATE---")
    
    question = state["question"]
    documents = state["documents"]

    response = generation_chain.invoke({"question": question, "context": documents})
    
    return {"generation": response}