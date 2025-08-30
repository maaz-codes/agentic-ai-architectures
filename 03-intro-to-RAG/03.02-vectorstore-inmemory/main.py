import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


load_dotenv()


def main():
    print("Hello from Vectorstore-in-memory!")

    pdf_path = "/Users/maakhan/Desktop/langchain-course/03-intro-to-RAG/03.02-vectorstore-inmemory/react-agent.pdf"
    loader = PyPDFLoader(file_path=pdf_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50, separator='\n')
    docs = text_splitter.split_documents(documents=documents)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index_react")

    new_vectorstore = FAISS.load_local("faiss_index_react", embeddings, allow_dangerous_deserialization=True)

    rag_prompt = hub.pull('langchain-ai/retrieval-qa-chat')
    llm = ChatOpenAI()
    feed_llm = create_stuff_documents_chain(llm, rag_prompt)
    chain = create_retrieval_chain(new_vectorstore.as_retriever(), feed_llm)

    result = chain.invoke({"input": "Give me gist of ReAct in 3 sentences"})
    print(result['answer'])

if __name__ == "__main__":
    main()
