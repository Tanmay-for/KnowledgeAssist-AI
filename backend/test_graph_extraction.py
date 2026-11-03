from backend.app.graph.graph_extraction import (
    build_graph_from_text
)


sample_text = """
Object-Oriented Programming uses classes and objects.

A class is a blueprint for creating objects.

Inheritance allows a class to acquire properties
from another class.

Polymorphism allows functions to behave differently.
Encapsulation protects data.
"""


result = build_graph_from_text(sample_text)

print("Automatic Graph Extraction Successful!")

print("\nExtracted Concepts:")

for concept in result["concepts"]:
    print("-", concept)

print("\nExtracted Relationships:")

for relationship in result["relationships"]:
    print(
        relationship["source"],
        "->",
        relationship["relationship"],
        "->",
        relationship["target"]
    )