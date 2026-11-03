
import backend.app.graph.knowledge_graph as kg

ROOT = "Object-Oriented Programming"

# Main OOP concepts that should connect to the root.
MAIN_CONCEPTS = [
    "Class",
    "Encapsulation",
    "Inheritance",
    "Polymorphism",
    "Abstraction",
    "Constructor",
    "Destructor",
]


def connect_root():
    kg.load_graph()

    if ROOT not in kg.graph:
        raise ValueError(
            "OOP root node not found. Rebuild the graph first."
        )

    print("Existing nodes:", kg.graph.number_of_nodes())
    print("Existing relationships:", kg.graph.number_of_edges())

    added = 0

    for concept in MAIN_CONCEPTS:

        if concept not in kg.graph:
            print(f"Skipping missing concept: {concept}")
            continue

        # Reuse the real document IDs associated with this concept.
        document_ids = kg.graph.nodes[concept].get(
            "document_ids", []
        )

        if not document_ids:
            print(f"Warning: No document IDs for {concept}")
            continue

        for document_id in document_ids:

            # Record the root's document association.
            kg.add_concept(ROOT, document_id)

            # Add the root-to-concept relationship.
            kg.add_relationship(
                ROOT,
                concept,
                "includes",
                document_id
            )

        added += 1
        print(f"Connected: {ROOT} -> {concept}")

    kg.save_graph()

    print("\nKnowledge Graph repaired successfully.")
    print("Total nodes:", kg.graph.number_of_nodes())
    print("Total relationships:", kg.graph.number_of_edges())

    print("\nRoot connections:")
    for source, target, data in kg.graph.out_edges(
        ROOT, data=True
    ):
        print(
            f"{source} -> {target} "
            f"({data.get('relationship')})"
        )


if __name__ == "__main__":
    connect_root()
