
from pathlib import Path

import backend.app.graph.knowledge_graph as kg

from backend.app.graph.graph_extraction import build_graph_from_text
from backend.app.services.document_registry import load_documents
from backend.app.services.document_service import process_document


def rebuild_knowledge_graph():
    documents = load_documents()

    # Reset the actual graph module's graph
    kg.graph.clear()
    kg.save_graph()

    successful = 0
    skipped = 0

    for document in documents:
        file_path = Path(document.get("file_path", ""))
        document_id = document.get("document_id")

        if not file_path.exists() or not document_id:
            print(f"Skipping: {file_path}")
            skipped += 1
            continue

        try:
            result = process_document(str(file_path))

            full_text = "\n".join(
                page["text"] for page in result["pages"]
            )

            graph_result = build_graph_from_text(
                full_text,
                document_id
            )

            successful += 1

            print(f"\nProcessed: {document['original_filename']}")
            print(f"Concepts: {len(graph_result['concepts'])}")
            print(
                f"Relationships: "
                f"{len(graph_result['relationships'])}"
            )

        except Exception as error:
            print(f"Failed: {file_path.name}: {error}")
            skipped += 1

    kg.save_graph()

    print("\nKnowledge Graph migration completed.")
    print("Successfully processed:", successful)
    print("Skipped:", skipped)
    print("Total graph concepts:", kg.graph.number_of_nodes())
    print("Total graph relationships:", kg.graph.number_of_edges())


if __name__ == "__main__":
    rebuild_knowledge_graph()
