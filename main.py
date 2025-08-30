import os

from dotenv import load_dotenv
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


load_dotenv()


def main():
    print("Hello from Retrieval!")

    embeddings = OpenAIEmbeddings() 
    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')

    query = "what is pinecone in Machine Learning?"
    chain = (
        PromptTemplate.from_template(template=query)
        | llm
    )
    # result = chain.invoke(input={})
    # print(result.content)

    vectorstore = PineconeVectorStore(
        index_name=os.environ['PINECONE_INDEX_NAME'],
        embedding=embeddings,
    )

    retrieval_qa_chat_prompt = hub.pull('langchain-ai/retrieval-qa-chat')
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), 
        combine_docs_chain=combine_docs_chain,
    )

    result = retrieval_chain.invoke(input={"input": query})
    print("Type: ", type(result))
    print(result['answer'])

if __name__ == "__main__":
    main()
