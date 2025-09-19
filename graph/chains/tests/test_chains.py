from dotenv import load_dotenv
from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from ingestion_pinecone import retriver
from graph.chains.generation import generation_chain
from graph.chains.hallucination_grader import hallucination_grader
from graph.chains.question_router import question_router
from pprint import pprint


load_dotenv()


def test_retrieval_grader_answer_yes() -> None:
    question = "agent memory"
    docs = retriver.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "yes"


def test_retrieval_grader_answer_no() -> None:
    question = "making pizza"
    docs = retriver.invoke(question)
    doc_txt = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score == "no"


def test_generation_chain():
    question = "agent memory"
    context = retriver.invoke(question)
    
    response = generation_chain.invoke({"question": question, "context": context})
    pprint(response)
    assert response


def test_hallucination_grader_answer_no():
    question = "What are the new ways to create LLM applications?"
    documents = "Recent advancements in LLM application development include using orchestration frameworks like LangChain and LlamaIndex, which allow for modular construction of LLM apps. Also, there is a trend towards using LLMs in multi-agent systems where multiple LLMs work together."
    generation = "New approaches for creating LLM applications involve orchestration frameworks such as LangChain and LlamaIndex for modular development, along with implementing multi-agent systems where multiple LLMs collaborate."
    
    response = hallucination_grader.invoke(input={
        "question": question,
        "documents": documents,
        "generation": generation,
    })
    print(response)

    assert response.has_hallucinated == False


def test_hallucination_grader_answer_yes():
    question = "What are the new ways to create LLM applications?"
    documents = "Recent advancements in LLM application development include using orchestration frameworks like LangChain and LlamaIndex, which allow for modular construction of LLM apps. Also, there is a trend towards using LLMs in multi-agent systems where multiple LLMs work together."
    generation_hard = "The latest methods include using quantum computing to boost LLM inference speeds and neural-symbolic AI integration, alongside orchestration frameworks like LangChain. Additionally, blockchain-based verification is becoming popular for LLM outputs."
    generation_easy = "Cats love eating pizzas with pineapples."

    response = hallucination_grader.invoke({
        "question": question,
        "documents": documents,
        "generation": generation_easy,
    })
    print(response)

    assert response.has_hallucinated == True


def test_question_router_answer_vectorstore():
    question = "agent memory"

    response = question_router.invoke({"question": question})
    assert response.datasource == "vectorstore"


def test_question_router_answer_websearch():
    question = "how to make pizza the rigth way."

    response = question_router.invoke({"question": question})
    assert response.datasource == "websearch"
