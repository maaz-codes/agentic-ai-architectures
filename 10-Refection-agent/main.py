from typing import List, Sequence, Dict
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph, MessagesState

from chains import generation_chain, reflection_chain


load_dotenv()


REFLECT="reflect"
GENERATE="generate"
LAST=-1


def generation_node(state: MessagesState) -> Dict:
    messages = state["messages"]
    response = generation_chain.invoke({"messages": messages})
    return {"messages": [response]}


def reflection_node(state: MessagesState) -> Dict:
    messages = state["messages"]
    response = reflection_chain.invoke({"messages": messages})
    return {"messages": [HumanMessage(content=response.content)]}


def should_continue(state: List[BaseMessage]) -> str:
    if len(state["messages"]) > 2:
        return END
    return REFLECT


def main():
    print("Hello from Reflection Agent!")

    builder = StateGraph(state_schema=MessagesState)
    builder.add_node(GENERATE, generation_node)
    builder.add_node(REFLECT, reflection_node)

    builder.set_entry_point(GENERATE)
    builder.add_conditional_edges(GENERATE, should_continue, {END: END, REFLECT: REFLECT})
    builder.add_edge(REFLECT, GENERATE)

    app = builder.compile()

    app.get_graph().draw_mermaid_png(output_file_path='graph.png')
    print("Graph saved!")

    query = """Make this tweet better:
    The German football team Borussia Dortmund is now starting an investigation into one of its own players for having expressed support for Charlie Kirk.
    What's going on in Europe???
    """
    response = app.invoke({"messages": [HumanMessage(content=query)]})
    print(response["messages"][LAST].content)



if __name__ == "__main__":
    main()
