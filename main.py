from dotenv import load_dotenv
from typing import List, Union

from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain_core.agents import AgentAction, AgentFinish
from langchain.tools import Tool
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser


load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""

    text = text.strip("'\n").strip('"')
    return len(text)

def get_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found!")


def main():
    print("Hello from langChain!")

    tools = [get_text_length]
    template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Begin!

        Question: {input}
        Thought:
    """ 

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), 
        tool_names=", ".join([t.name for t in tools]),
    )
 
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', stop=['\nObservation:'])
    agent = {"input": lambda x: x['input']} | prompt | llm | ReActSingleInputOutputParser()
    query = "What is the text length of the word 'DOG' in characters?"
    
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input": query})

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = get_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        print(f"Observation: {observation}")


if __name__ == "__main__":
    main()
