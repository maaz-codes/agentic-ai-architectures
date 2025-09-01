import os
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain import hub


load_dotenv()

def run_llm(query: str):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
    vectorstore = PineconeVectorStore(index_name=os.environ.get('PINECONE_INDEX_NAME'), embedding=embeddings)
    chat = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    rag_prompt = hub.pull('langchain-ai/retrieval-qa-chat')
    augment_docs_chain = create_stuff_documents_chain(chat, rag_prompt)
    qa = create_retrieval_chain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=augment_docs_chain,
    ) 
    result = qa.invoke(input={"input": query})

    return result


def main():
    print("Hello from Retrieval!")
    response = run_llm(query="What is Langchain Chain?")
    print(response['answer'])
    

if __name__ == "__main__":
    main()
