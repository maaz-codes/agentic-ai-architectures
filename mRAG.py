from dotenv import load_env
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage


load_env()


def load_existing_vector_store(persist_directory="dbv1/chroma_db"):
    """Load existing ChromaDB vector store from disk"""
    print(f"📁 Loading existing vector store from {persist_directory}...")
    
    # Initialize the same embedding model that was used to create the store
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Load the existing vector store
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model
    )
    
    print("✅ Vector store loaded successfully!")
    return vectorstore


def generate_final_answer(llm, chunks, query):
    """Generate final answer using multimodal content"""
    
    try:
        # Initialize LLM (needs vision model for images)
        # llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        # Build the documents content string
        documents_content = ""
        for i, chunk in enumerate(chunks):
            documents_content += f"--- Document {i+1} ---\n"
            
            if "original_content" in chunk.metadata:
                original_data = json.loads(chunk.metadata["original_content"])
                
                # Add raw text
                raw_text = original_data.get("raw_text", "")
                if raw_text:
                    documents_content += f"TEXT:\n{raw_text}\n\n"
                
                # Add tables as HTML
                tables_html = original_data.get("tables_html", [])
                if tables_html:
                    documents_content += "TABLES:\n"
                    for j, table in enumerate(tables_html):
                        documents_content += f"Table {j+1}:\n{table}\n\n"
            
            documents_content += "\n"
        
        # Create the prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant that analyzes documents containing text, tables, and images to answer questions accurately."),
            ("human", """Based on the following documents, please answer this question: {query}

CONTENT TO ANALYZE:
{documents_content}

Please provide a clear, comprehensive answer using the text, tables, and images above. If the documents don't contain sufficient information to answer the question, say "I don't have enough information to answer that question based on the provided documents."

ANSWER:""")
        ])
        
        # Get the prompt text using the template
        formatted_messages = prompt_template.format_messages(
            query=query,
            documents_content=documents_content
        )
        prompt_text = formatted_messages[1].content  # Get human message content

        # Build message content starting with text (same structure as original)
        message_content = [{"type": "text", "text": prompt_text}]
        
        # Add all images from all chunks (unchanged from original)
        for chunk in chunks:
            if "original_content" in chunk.metadata:
                original_data = json.loads(chunk.metadata["original_content"])
                images_base64 = original_data.get("images_base64", [])
                
                for image_base64 in images_base64:
                    message_content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                    })
        
        # Send to AI and get response (unchanged from original)
        message = HumanMessage(content=message_content)
        response = llm.invoke([message])
        
        return response.content
        
    except Exception as e:
        print(f"❌ Answer generation failed: {e}")
        return "Sorry, I encountered an error while generating the answer."


def main():
    db = load_existing_vector_store(persist_directory="/Users/mac/Desktop/langchain-learn/dbv2")

    query = "What are the two main components of the Transformer architecture?"
    retriever = db.as_retriever(seach_kwargs={"k": 3})
    chunks = retriever.invoke(query)

    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    answer =  generate_final_answer(llm=llm, chunks=chunks, query=query)
    print(answer)


if __name__ == '__main__':
    main()
