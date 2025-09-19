from graph.graph import graph

def main():
    print("Hello from CRAG!")

    question = "What is the difference between langchain and langgraph?"
    result = graph.invoke(input=
        {
            "question": question
        }
    )
    print(result["generation"])


if __name__ == "__main__":
    main()
