from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from lc_logger import MyLogger


load_dotenv()
my_logger = MyLogger()


csv_file = 'seinfield.csv'
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
llm = ChatOpenAI(model='gpt-4o', temperature=0)

create_code_agent = create_react_agent(
    prompt=prompt,
    llm=llm,
    tools=tools,
)

csv_agent = create_csv_agent(
    llm=llm,
    path=csv_file,
    verbose=True,
    allow_dangerous_code=True,
)

code_agent = AgentExecutor(
    agent=create_code_agent, 
    tools=tools, 
    verbose=True,
    callbacks=[my_logger],
)


def main():
    print("Hello from Code Interpreter!")

    code_agent.invoke(
        input={
            "input": """
                Generate and save in current working directory 1 QRcode that points to www.udemy.com.
                You have the qrcode package already installed.
            """
        }
    )

    csv_agent.invoke(input="Which writer wrote the most episodes in file seinfield.csv")


if __name__ == "__main__":
    main()
