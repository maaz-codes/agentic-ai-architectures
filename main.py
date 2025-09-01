from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_experimental.tools.python.tool import PythonREPLTool


load_dotenv()


def main():
    print("Hello from Code Interpreter!")

    base_prompt = hub.pull('langchain-ai/react-agent-template')
    instructions = """
        You are an agent designed to write and execute python code to answer questions.
        You have access to a python REPL, which you can use to execute python code.
        If you get an error, debug your code and try again.
        Only use the output of your code to answer the question.
        You might know the answer without running any code, but you should still run the code to get the answer.
        If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    tools = [PythonREPLTool()]
    tool_names = [tool.name for tool in tools]

    prompt = base_prompt.partial(instructions=instructions)
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)

    agent = create_react_agent(
        prompt=prompt,
        llm=llm,
        tools=tools
    )

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    agent_executor.invoke(
        input={
            "input": """
                Generate and save in current working directory 1 QRcode that points to www.udemy.com.
                You have the qrcode package already installed.
            """
        }
    )






if __name__ == "__main__":
    main()
