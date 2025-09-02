from typing import Any
from dotenv import load_dotenv
from langchain.agents.react.agent import create_react_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_core.tools import Tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from agents import code_agent, csv_agent
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from lc_logger import MyLogger


load_dotenv()


def code_agent_wrapper(prompt: str) -> dict[str, Any]:
    return code_agent.invoke(input={"input": prompt})


def main():
    print("Hello from Router Agent!")


    tools = [
        Tool(
            name="python_agent",
            func=code_agent_wrapper,
            description="""
                Takes ONLY natural language requests and converts them to Python code internally.
                Input should be plain English like: 'generate a code for calculator app'
                DO NOT pass Python code - pass the user's original natural language request.
                This tool will handle the code generation and execution internally.
            """
        ),
        Tool(
            name="csv_agent",
            func=csv_agent.invoke,
            description="""
                useful when you need to answer question over seinfield.csv file,
                takes an input the entire question and returns the answer after running pandas calculations.
            """
        ),
    ]

    base_prompt = hub.pull('langchain-ai/react-agent-template')
    prompt = base_prompt.partial(instructions="")
    llm = ChatOpenAI(model='gpt-4o', temperature=0)

    tool_calling_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you're a helpful assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    my_logger = MyLogger()

    # create_router_agent = create_react_agent(
    #     prompt=prompt,
    #     llm=llm,
    #     tools=tools,
    # )

    create_router_agent = create_tool_calling_agent(
        prompt=tool_calling_prompt,
        llm=llm,
        tools=tools,
    )

    router_agent = AgentExecutor(
        agent=create_router_agent, 
        tools=tools, 
        verbose=True,
        # callbacks=[my_logger]
    )

    # res = router_agent.invoke(input={"input": "Which season has the most episodes?"})
    res = router_agent.invoke(input={"input": "Generate a qr code for this link: www.python.langchain.com"})
    print(res)

if __name__ == "__main__":
    main()
