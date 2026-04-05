from typing import List
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langgraph.graph import END, MessagesState, StateGraph

from chains import revise_responder_chain, first_responder_chain
from tool_executor import execute_tools


load_dotenv()


MAX_ITERATIONS=2
DRAFT="draft"
TOOLS="tools"
REVISE="revise"
LAST=-1


def draft_node(state: MessagesState) -> dict:
    messages = state["messages"]
    response = first_responder_chain.invoke({
        "messages": messages
    })

    return {"messages": [response]}


def revise_node(state: MessagesState) -> dict:
    messages = state["messages"]
    response = revise_responder_chain.invoke({
        "messages": messages
    })
    return {"messages": [response]}


def event_loop(state: MessagesState) -> dict:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state["messages"])
    if count_tool_visits > MAX_ITERATIONS:
        return END
    return TOOLS


def main():
    print("Hello from Reflexion Agent!")

    builder = StateGraph(MessagesState)

    builder.add_node(DRAFT, draft_node)
    builder.add_node(TOOLS, execute_tools)
    builder.add_node(REVISE, revise_node)

    builder.set_entry_point(DRAFT)
    builder.add_edge(DRAFT, TOOLS)
    builder.add_edge(TOOLS, REVISE)
    builder.add_conditional_edges(REVISE, event_loop, {END:END, TOOLS:TOOLS})

    graph = builder.compile()
    graph.get_graph().draw_mermaid_png(output_file_path='graph.png')

    query = """Write about AI-Powered Soc / autonomous soc problem domain, 
    list startups that do that and raised capital."""
    
    response = graph.invoke(input={
        "messages": [HumanMessage(content=query)]
    })

    ai_response = response["messages"][LAST].tool_calls[0]['args']
    print(ai_response['answer'])


if __name__ == "__main__":
    main()
