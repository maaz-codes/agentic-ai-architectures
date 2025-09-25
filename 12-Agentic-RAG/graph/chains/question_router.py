from dotenv import load_dotenv
from typing import Literal
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate


load_dotenv()


class QuestionRouter(BaseModel):
    datasource: Literal["websearch", "vectorstore"] = Field(
        description="Given a user question choose to route it to web search or a vectorstore."
    )


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(QuestionRouter)
system = """You are an expert at routing a user question to a vectorstore or web search.
The vectorstore contains documents related to agents, prompt engineering, and adversarial attacks.
Use the vectorstore for questions on these topics. For all else, use web-search."""

prompt_template = ChatPromptTemplate(
    [
        ("system", system),
        ("human", "{question}")
    ]
)

question_router = prompt_template | llm
