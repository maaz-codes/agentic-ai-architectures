from typing import Any, Dict
from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from graph.state import GraphState


def grade_documents(state: GraphState) -> Dict:
    """
    Determines whether the retrieved documents are relevant to the question,
    If any document is not relevant, we will set a flag to run web search.

    Args: 
        state (dicy): The current graph state
    
    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")

    douments = state["documents"]
    question = state["question"]

    filtered_docs = []
    should_web_search = False

    for doc in douments:
        score: GradeDocuments = retrieval_grader.invoke({"question": question, "document": doc.page_content})
        if score.binary_score == "yes":
            filtered_docs.append(doc)
        else:
            should_web_search = True
    
    return {
        "documents": filtered_docs,
        "web_search": should_web_search
    }
    