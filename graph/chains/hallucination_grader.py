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


def main():
    documents = "Recent advancements in LLM application development include using orchestration frameworks like LangChain and LlamaIndex, which allow for modular construction of LLM apps. Also, there is a trend towards using LLMs in multi-agent systems where multiple LLMs work together."
    correct_generation = "New approaches for creating LLM applications involve orchestration frameworks such as LangChain and LlamaIndex for modular development, along with implementing multi-agent systems where multiple LLMs collaborate."
    hallucinated_generation = "The latest methods include using quantum computing to boost LLM inference speeds and neural-symbolic AI integration, alongside orchestration frameworks like LangChain. Additionally, blockchain-based verification is becoming popular for LLM outputs."
    
    response = hallucination_grader.invoke(input={
        "question": "What are the new ways to create LLM applications?",
        "documents": documents,
        "generation": hallucinated_generation,
    })
    print(response)


if __name__ == "__main__":
    main()