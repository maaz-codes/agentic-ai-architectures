from graph.graph import graph


def test_crag_decision_generate():
    question = "What is agent memory?"
    result = graph.invoke(input=
        {
            "question": question
        }
    )
    print(result["generation"])
    assert result["generation"] and result["web_search"] == False


def test_crag_decision_web_search():
    question = "What is the difference between langchain and langgraph?"
    result = graph.invoke(input=
        {
            "question": question
        }
    )
    print(result["generation"])
    assert result["generation"] and result["web_search"] == True
