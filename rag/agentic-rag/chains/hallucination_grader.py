from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate


load_dotenv()


class Hallucination_grade(BaseModel):
    """Stores where the LLM Hallucinated or not."""

    has_hallucinated: bool = Field(
        description="Answer addresses the question, 'yes' or 'no'"
    )

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(Hallucination_grade)

system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
prompt_template = ChatPromptTemplate(
    [
        ("system", system),
        ("human", "Question: {question}\n\nContext Documents: {documents}\n\nLLM Generation: {generation}"),
    ]
)

hallucination_grader = prompt_template | llm
