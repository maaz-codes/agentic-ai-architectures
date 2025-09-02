from typing import Any
from dotenv import load_dotenv
from langchain.agents.react.agent import create_react_agent
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from langchain_core.tools import Tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from agents import code_agent, csv_agent
from lc_logger import MyLogger


load_dotenv()

def code_agent_wrapper(prompt: str) -> dict[str, Any]:
    return code_agent.invoke(input={"input": prompt})


def main():
    print("Hello from Code Interpreter!")


    tools = [
        Tool(
            name="Python Agent",
            func=code_agent_wrapper,
            description="""
                useful when you need to transform natural language to python and execute the python code,
                returning the results of the code execution.
                DOES NOT ACCEPT CODE AS INPUT.
            """
        ),
        Tool(
            name="CSV Agent",
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

    my_logger = MyLogger()

    create_router_agent = create_react_agent(
        prompt=prompt,
        llm=llm,
        tools=tools,
    )

    router_agent = AgentExecutor(
        agent=create_router_agent, 
        tools=tools, 
        verbose=True,
        callbacks=[my_logger]
    )

    # res = router_agent.invoke(input={"input": "Which season has the most episodes?"})
    res = router_agent.invoke(input={"input": "Generate a qr code for this link: www.python.langchain.com"})
    print(res)

if __name__ == "__main__":
    main()
