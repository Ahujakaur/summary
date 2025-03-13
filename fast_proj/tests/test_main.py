from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_query_endpoint():
    response = client.post("/query", json={"query": "test query"})
    assert response.status_code == 200
    assert response.json()["query"] == "test query"

def test_summarize_endpoint():
    text = "This is a very long text that needs to be summarized. " * 20
    response = client.post("/summarize", json={
        "text": text,
        "max_length": 130,
        "min_length": 30
    })
    assert response.status_code == 200
    assert "summary" in response.json()                                                                                                                                                                                                                                                                                                                                                                                                                                 
    test_text = """
    Python is a high-level, general-purpose programming language. Python's design philosophy 
    emphasizes code readability with the use of significant indentation. Python is dynamically 
    typed and garbage-collected. It supports multiple programming paradigms, including structured, 
    object-oriented and functional programming. It is often described as a "batteries included" 
    language due to its comprehensive standard library.
    """                                                                                                                                                                                                                                                     
    
    
    short_text = "This is too short to summarize."
    
    long_text = """
    Python is a high-level, general-purpose programming language. Python's design philosophy 
    emphasizes code readability with the use of significant indentation. Python is dynamically 
    typed and garbage-collected. It supports multiple programming paradigms, including structured, 
    object-oriented and functional programming. It is often described as a "batteries included" 
    language due to its comprehensive standard library. Python was created by Guido van Rossum 
    and was first released in 1991. Python consistently ranks as one of the most popular 
    programming languages. Python's development is managed by the non-profit Python Software 
    Foundation. Python features a dynamic type system and automatic memory management. It supports 
    multiple programming paradigms, including object-oriented, imperative, functional and procedural.
    """ * 3  

    test_cases = [
        {
            "name": "basic_summarization",
            "data": {
                "text": test_text,
                "max_length": 130,
                "min_length": 30
            },
            "expected_status": 200
        },
        {
            "name": "short_text_error",
            "data": {
                "text": short_text,
                "max_length": 130,
                "min_length": 30
            },
            "expected_status": 400
        },
        {
            "name": "long_text",
            "data": {
                "text": long_text,
                "max_length": 150,
                "min_length": 50
            },
            "expected_status": 200
        },
        {
            "name": "custom_length_params",
            "data": {
                "text": test_text,
                "max_length": 200,
                "min_length": 50
            },
            "expected_status": 200
        }
    ]
    
    def test_summarize_endpoint():
        for case in test_cases:
            response = client.post("/summarize", json=case["data"])
            assert response.status_code == case["expected_status"]
            
            if response.status_code == 200:
                assert "summary" in response.json()
                assert "original_length" in response.json()
                assert "summary_length" in response.json()
                assert len(response.json()["summary"]) > 0
                if case["data"]["max_length"]:
                    assert len(response.json()["summary"]) <= case["data"]["max_length"]