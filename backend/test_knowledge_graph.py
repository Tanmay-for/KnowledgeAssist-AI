from backend.app.graph.knowledge_graph import (
    add_concept,
    add_relationship,
    get_related_concepts,
    save_graph,
    load_graph
)


# Add concepts
add_concept("Object-Oriented Programming")
add_concept("Class")
add_concept("Object")
add_concept("Inheritance")
add_concept("Polymorphism")


# Add relationships
add_relationship(
    "Object-Oriented Programming",
    "Class",
    "contains"
)

add_relationship(
    "Object-Oriented Programming",
    "Object",
    "contains"
)

add_relationship(
    "Class",
    "Inheritance",
    "supports"
)

add_relationship(
    "Class",
    "Polymorphism",
    "supports"
)


# Test graph
print("Knowledge Graph created successfully!")

print("\nRelated concepts:")

related = get_related_concepts(
    "Object-Oriented Programming"
)

for item in related:
    print(
        item["concept"],
        "->",
        item["relationship"]
    )


# Save graph
file_path = save_graph()

print("\nGraph saved at:", file_path)


# Test loading
total_nodes = load_graph()

print("Total concepts:", total_nodes)

print("\nKnowledge Graph test completed!")