import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from agent_tools.tools import get_profile_url_tavily


load_dotenv()


def linkedin_lookup(name: str) -> str:
    print("Hello from lookup!")    

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    template = """
        given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
        Your answer should contain only a URL or NOT FOUND, if you didn't find any URL.
        Answer should not be in braces or anything, either the URL or the string NOT FOUND.
    """ 
    prompt_template = PromptTemplate(
        template=template,
        input_variables=['name_of_person']
    )
    tools = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get Linkedin Page URL",
        )
    ]
    create_agent = create_react_agent(
        prompt=hub.pull('hwchase17/react'),
        llm=llm,
        tools=tools,
    )
    agent = AgentExecutor(
        agent=create_agent,
        tools=tools,
        verbose=True,
    )

    result = agent.invoke(
        input={
            "input": prompt_template.format_prompt(name_of_person=name)
        }
    )
    linkedin_profile_url = result['output']
    return linkedin_profile_url


def main():
    name = 'Maaz Khan'
    print(lookup(name))


if __name__ == "__main__":
    main()