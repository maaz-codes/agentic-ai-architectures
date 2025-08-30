import os

from dotenv import load_dotenv
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough


load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    print("Hello from Retrieval!")

    query = "what is pinecone in Machine Learning?"
    template = """
        Use the following pieces of context to answer the questions at the end.
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Use three sentences maximum and keep the answer as concise as possible.
        Always say "thanks for asking!" at the end of the answer.

        {context}

        Question: {question}

        Helpful Answer:
    """ 
    
    embeddings = OpenAIEmbeddings() 
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')
    custom_rag_prompt = PromptTemplate.from_template(template)

    vectorstore = PineconeVectorStore(
        index_name=os.environ['PINECONE_INDEX_NAME'],
        embedding=embeddings,
    )

    rag_chain = (
        {   
            "context": vectorstore.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
        } 
        | custom_rag_prompt
        | llm
    )

    result = rag_chain.invoke(query)
    print("type:", type(result))
    print(result)


    # retrieval_qa_chat_prompt = hub.pull('langchain-ai/retrieval-qa-chat')
    # combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    # retrieval_chain = create_retrieval_chain(
    #     retriever=vectorstore.as_retriever(), 
    #     combine_docs_chain=combine_docs_chain,
    # )

    # result = retrieval_chain.invoke(input={"input": query})
    # print(result['answer'])

if __name__ == "__main__":
    main()
