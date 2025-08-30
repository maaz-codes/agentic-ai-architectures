import os
from unittest import loader
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from openai import embeddings
from langchain.prompts import PromptTemplate


load_dotenv()


def main():
    print("Hello from Retrieval!")

    embeddings = OpenAIEmbeddings() 
    llm = ChatOpenAI()

    query = "what is pinecone in Machine Learning?"
    chain = (
        PromptTemplate.from_template(template=query)
        | llm
    )
    result = chain.invoke(input={})
    print(result.content)

if __name__ == "__main__":
    main()
