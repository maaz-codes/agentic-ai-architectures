import os
from unittest import loader
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


load_dotenv()


def main():
    print("Hello from Ingestion!")

    print("Loading...")
    loader = TextLoader(os.path.join(os.path.dirname(__file__), "vector-medium-blog-1.txt"))
    document = loader.load()

    print("Splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks!")

    print("Embedding...")
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

    print("Storing...")
    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.environ.get('PINECONE_INDEX_NAME'))

    print("\n\nFinished!")

if __name__ == "__main__":
    main()
