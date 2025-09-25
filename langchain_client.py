import asyncio
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools


load_dotenv()


async def main():
    print("Hello from Client!")

    client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["/Users/maakhan/Desktop/langchain-course/servers/math_server.py"],
            "transport": "stdio",
        }
    }
    )
    llm = ChatOpenAI()
    with client.session("math") as session:
        tools = await load_mcp_tools(session)
    agent = create_react_agent(llm, tools)
    response = await agent.invoke({"messages": "What's (3 + 3)?"})
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
