from typing import Dict
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from graph.state import GraphState


load_dotenv()


def web_search(state: GraphState) -> Dict:
    print("---WEB SEARCHING---")

    web_search_tool = TavilySearch(max_results=3)
    question = state["question"]
    documents = state["documents"]

    # llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools=tools, tool_choice="TavilySearch")
    tavily_results = web_search_tool.invoke({"query": question})
    joined_tavily_results = "\n".join(
        [tavily_result["content"] for tavily_result in tavily_results["results"]]
    )
    web_results = Document(page_content=joined_tavily_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents}




if __name__ == "__main__":
    state = web_search(
        state={
            "question": "agent memory is crutial",
            "documents": None,
        }
    )

    print(state)