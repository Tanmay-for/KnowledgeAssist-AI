
from backend.app.rag.retriever import retrieve_relevant_chunks

question = "What is a class in C++?"

try:
    results = retrieve_relevant_chunks(question, top_k=3)

    print("Retrieval successful!")
    print("Question:", question)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Filename:", result["filename"])
        print("Page:", result["page"])
        print("Distance:", result["distance"])
        print("Content:", result["text"])

except Exception as error:
    print("Error:", error)
