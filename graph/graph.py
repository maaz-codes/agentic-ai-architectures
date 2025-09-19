from dotenv import load_dotenv
from langgraph.graph import START, END, StateGraph
from regex import P
from graph.state import GraphState
from graph.consts import *
from graph.nodes import *
from graph.chains.hallucination_grader import Hallucination_grade, hallucination_grader
from graph.chains.question_router import question_router, QuestionRouter


load_dotenv()


def should_web_search(state: GraphState):
    print("---DECISION NODE---")

    if state["web_search"]:
        print("-DECIDED: WEB_SEARCH-")
        return WEB_SEARCH
    print("-DECIDED: GENERATE-")
    return GENERATE


def grade_generation(state: GraphState):
    print("---GRADING GENERATION---")

    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]

    score: Hallucination_grade = hallucination_grader.invoke(
        {
            "question": question,
            "documents": documents, 
            "generation": generation,
        }
    )

    if score.has_hallucinated:
        print("--DECISION: DO WEB_SEARCH AGAIN--")
        return "not useful"
    else:
        print("--DECISION: READY FOR FINAL ANSWER--")
        return "useful"
    

def query_router(state: GraphState):
    print("---ROUTER DECIDING---")
    question = state["question"]
    datasource: QuestionRouter = question_router.invoke({"question": question})

    if datasource == "websearch":
        print("--DECIDED: WEB SEARCH--")
        return WEB_SEARCH
    print("--DECIDED: RETRIEVE--")
    return RETRIEVE


builder = StateGraph(GraphState)

builder.add_node(GENERATE, generate)
builder.add_node(RETRIEVE, retrieve)
builder.add_node(WEB_SEARCH, web_search)
builder.add_node(GRADE_DOCUMENTS, grade_documents)

# builder.set_entry_point(RETRIEVE)
builder.add_conditional_edges(
    START, 
    query_router, 
    {RETRIEVE:RETRIEVE, WEB_SEARCH:WEB_SEARCH}
)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.add_conditional_edges(
    GRADE_DOCUMENTS, 
    should_web_search, 
    {WEB_SEARCH:WEB_SEARCH, GENERATE:GENERATE}
)
builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_edge(GENERATE, END)
builder.add_conditional_edges(
    GENERATE, 
    grade_generation,
    {"useful": END, "not useful": WEB_SEARCH}
)

graph = builder.compile()
# graph.get_graph().draw_mermaid_png(output_file_path='graph.png')
