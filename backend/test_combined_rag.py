from backend.app.rag.rag_pipeline import answer_question

question = "Explain classes and objects in C++."

print("=" * 50)
print("KNOWLEDGEASSIST AI - COMBINED RAG TEST")
print("=" * 50)

result = answer_question(
    question=question,
    mode="exam",
    top_k=5
)

print("\nQUESTION:")
print(question)

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nDOCUMENT SOURCES:")

for source in result["sources"]:
    print(
        f"File: {source['filename']} | "
        f"Page: {source['page']}"
    )

print("\nKNOWLEDGE GRAPH RESULTS:")

for item in result["graph_context"]:
    print("\nConcept:", item["concept"])

    for related in item["related_concepts"]:
        print(
            "Relationship:",
            related["relationship"],
            "->",
            related["concept"]
        )

print("\n" + "=" * 50)
print("COMBINED RAG TEST COMPLETED")
print("=" * 50)