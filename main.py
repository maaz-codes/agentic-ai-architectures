import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

stdio_server_params = StdioServerParameters(
    command="python",
    args=["/Users/maakhan/Desktop/langchain-course/servers/math_server.py"],
)


async def main():
    print("Hello from MCP!")
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Session Initialized!")
            tools = await load_mcp_tools(session)
            # tools = []
            agent = create_react_agent(llm, tools)

            print(tools)
            result = agent.invoke({"messages": [HumanMessage(content="What is 2 + 2 ?")]})
            print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
