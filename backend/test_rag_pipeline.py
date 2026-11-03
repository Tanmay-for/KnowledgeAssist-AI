
from backend.app.rag.rag_pipeline import answer_question


question = "What is a class in C++?"

try:
    print("Running KnowledgeAssist AI RAG Pipeline...\n")

    result = answer_question(
        question=question,
        mode="exam",
        top_k=5
    )

    print("QUESTION:")
    print(question)

    print("\nGENERATED ANSWER:")
    print("=" * 50)
    print(result["answer"])

    print("\nSOURCE DOCUMENTS:")
    print("=" * 50)

    for source in result["sources"]:
        print("Filename:", source["filename"])
        print("Page:", source["page"])

    print("\nRAG Pipeline test completed successfully!")

except Exception as error:
    print("Error:", error)
