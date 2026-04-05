import os
from typing import List

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents.base  import Document
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings


load_dotenv()


def index_docs(documents: List[Document]) -> bool:
    try:
        vectorstore.add_documents(documents)
        print("Indexed successfully")
    except Exception as e:
        print(f"Indexing Failed: {e}")
        return False
    return True


def clean_metadata(doc):
    # only keeping source
    return {
        "source": doc.metadata.get("source")
    }


urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [doc for sublist in docs for doc in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, 
    chunk_overlap=0,
)

doc_splits = text_splitter.split_documents(docs_list)
docs_cleaned = [
    Document(page_content=d.page_content, metadata=clean_metadata(d))
    for d in doc_splits
]

embeddings = OpenAIEmbeddings(
    model='text-embedding-3-small',
    chunk_size=50,
    retry_min_seconds=10,
)

vectorstore = PineconeVectorStore(
    index_name=os.environ.get('PINECONE_INDEX_NAME'),
    embedding=embeddings,
)

retriver = vectorstore.as_retriever()


def main():
    index_docs(docs_cleaned)


if __name__ == "__main__":
    main()
