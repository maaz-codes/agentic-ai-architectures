import os
import ssl
import certifi
import asyncio
from typing import List
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langsmith import expect
from sqlalchemy import false


load_dotenv()

print("Hello from langchain-assistant!")

# Configure SSL context to use certifi certificates
ss_context = ssl.create_default_context(cafile=certifi.where())
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

embeddings = OpenAIEmbeddings(
    model='text-embedding-3-small',
    chunk_size=50,
    retry_min_seconds=10,
)

vectorstore = PineconeVectorStore(
    index_name=os.environ.get('PINECONE_INDEX_NAME'),
    embedding=embeddings,
)

tavily_extract = TavilyExtract()
tavily_map = TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl = TavilyCrawl()


async def index_documents_async(documents: List[Document], batch_size: int = 50):
    """Indexing the docs asynchronously"""

    print("VECTOR STORAGE PHASE")

    # Create batches
    batches = [documents[i: i + batch_size] for i in range(0, len(documents), batch_size)]

    async def add_batch(batch: List[Document], batch_num: int):
        try:
            await vectorstore.aadd_documents(batch)
            print(f"Vectorstore: Successfully added batch {batch_num}/{len(batches)} ({len(batch)} documents)")
        except Exception as e:
            print(f"Error Vectorstore: Failed to add batch {batch_num} - {e}")
            return False
        return True

    # Process batches concurrently    
    tasks = [add_batch(batch, i + 1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # counting successful batches
    successful = sum(1 for result in results if result is True)

    if successful == len(batches):
        print(f"Vectorstore: All batches processed successfully! ({successful}/{len(batches)})")
    else:
        print(f"Warning Vectorstore: Processed {successful}/{len(batches)} batches successfully")
    


async def main():
    """Main async function to orchestrate the entire process."""

    print("\nDOCUMENTATION INGESTION PIPELINE\n\n")

    print("TavilyCrawl: Starting to crawl documentation from https://python.langchain.com/\n")

    # Crawl Documentation site
    res = tavily_crawl.invoke({
        "url": "https://python.langchain.com/",
        "max_depth": 1,
        "extract_depth": "advanced",
    })
    pages = res['results']
    all_docs = [Document(page_content=page['raw_content'], metadata={"source": page['url']}) for page in pages]

    # Splitting of the data into chunks
    print("Splitting into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    all_chunks = text_splitter.split_documents(all_docs)
    print(f"Text Splitter: Created {len(all_chunks)} chunks from {len(all_docs)} documents.\n")

    await index_documents_async(all_chunks, batch_size=500)

    print("\n\nPIPELINE COMPLETED!\n")
    print("Documentation ingestion pipeline finished succesfully")
    print(f"    - URLs mapped: {len(pages)}")
    print(f"    - Documents extracted: {len(all_docs)}")
    print(f"    - Chunks created: {len(all_chunks)}")



if __name__ == "__main__":
    asyncio.run(main())
