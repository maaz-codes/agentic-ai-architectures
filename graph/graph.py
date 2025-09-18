from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.state import GraphState
from graph.consts import *
from graph.nodes import *

load_dotenv()


def should_web_search(state: GraphState):
    if state["web_search"]:
        return WEB_SEARCH
    return GENERATE

builder = StateGraph(GraphState)

builder.add_node(GENERATE, generate)
builder.add_node(RETRIEVE, retrieve)
builder.add_node(WEB_SEARCH, web_search)
builder.add_node(GRADE_DOCUMENTS, grade_documents)

builder.set_entry_point(RETRIEVE)
builder.add_edge(RETRIEVE, GRADE_DOCUMENTS)
builder.add_conditional_edges(
    GRADE_DOCUMENTS, 
    should_web_search, 
    {WEB_SEARCH:WEB_SEARCH, GENERATE:GENERATE}
)
builder.add_edge(WEB_SEARCH, GENERATE)
builder.add_edge(GENERATE, END)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path='graph.png')