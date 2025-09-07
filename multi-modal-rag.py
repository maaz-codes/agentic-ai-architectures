import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate

from partitioning import partition_document
from chunking import create_chunks_by_title
from utils import export_chunks_to_json
from summarizing import summarise_chunks
from vector_store import create_vector_store


load_dotenv()


def format_content(chunks):
    for i, chunk in enumerate(chunks):
        content = f"--- Document {i+1} ---\n"
        
        if "original_content" in chunk.metadata:
            original_data = json.loads(chunk.metadata["original_content"])
            
            # Add raw text
            raw_text = original_data.get("raw_text", "")
            if raw_text:
                content += f"TEXT:\n{raw_text}\n\n"
            
            # Add tables as HTML
            tables_html = original_data.get("tables_html", [])
            if tables_html:
                content += "TABLES:\n"
                for j, table in enumerate(tables_html):
                    content += f"Table {j+1}:\n{table}\n\n"
            
            content += "\n"


def main():
    print("\n\nHello from MRAG!\n")

    file_path = "/Users/maakhan/Desktop/langchain-course/docs/attention-is-all-you-need.pdf"
    elements = partition_document(file_path=file_path)
    chunks = create_chunks_by_title(elements)
    processed_chunks = summarise_chunks(chunks)
    db = create_vector_store(processed_chunks)

    # Retrieval
    query = "What are the two main components of the Transformer architecture?"
    retriever = db.as_retriever(seach_kwargs={"k": 3})
    chunks = retriever.invoke(query)

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    content = format_content(chunks)
    prompt_template = """Based on the following documents, please answer this question: {query}

        CONTENT TO ANALYZE:
        {content}

        Please provide a clear, comprehensive answer using the text, tables, and images above. If the documents don't contain sufficient information to answer the question, say "I don't have enough information to answer that question based on the provided documents."

        ANSWER:"""
    
    prompt = PromptTemplate(template=prompt_template).partial_variables(
        query=query,
        content=content
    )

    message_content = [{"type": "text", "text": prompt}]
        
    # Add all images from all chunks
    for chunk in chunks:
        if "original_content" in chunk.metadata:
            original_data = json.loads(chunk.metadata["original_content"])
            images_base64 = original_data.get("images_base64", [])
            
            for image_base64 in images_base64:
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                })
    
    # Send to AI and get response
    message = HumanMessage(content=message_content)
    response = llm.invoke([message])
    
    print(response.content)
    

    export_chunks_to_json(chunks, filename='rag_results.json')

    print("Sanity Checked!")


if __name__ == "__main__":
    main()
