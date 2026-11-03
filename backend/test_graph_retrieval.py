from backend.app.graph.knowledge_graph import (
    load_graph,
    search_graph
)

# Load previously saved graph
load_graph()

question = "Explain classes and objects in C++."

results = search_graph(question)

print("Knowledge Graph Retrieval Test")
print("=" * 40)

print("Question:", question)

for item in results:
    print("\nConcept:", item["concept"])

    for related in item["related_concepts"]:
        print(
            "Related:",
            related["concept"],
            "| Relationship:",
            related["relationship"]
        )

print("\nGraph retrieval test completed!")