
import networkx as nx
import json

from pathlib import Path
from backend.app.core.config import settings


# Create a directed knowledge graph
graph = nx.DiGraph()


def add_concept(concept: str, document_id: str):
    """Add a concept and track the document contributing it."""

    concept = concept.strip()

    if concept:
        graph.add_node(concept)

        document_ids = graph.nodes[concept].setdefault(
            "document_ids", []
        )

        if document_id not in document_ids:
            document_ids.append(document_id)


def add_relationship(
    source: str,
    target: str,
    relationship: str,
    document_id: str
):
    """Connect concepts and track the contributing document."""

    source = source.strip()
    target = target.strip()

    if source and target:
        graph.add_edge(source, target, relationship=relationship)

        document_ids = graph[source][target].setdefault(
            "document_ids", []
        )

        if document_id not in document_ids:
            document_ids.append(document_id)


def get_related_concepts(concept: str) -> list:
    """Find concepts connected to a given concept."""

    if concept not in graph:
        return []

    related = []

    for neighbor in graph.successors(concept):
        related.append({
            "concept": neighbor,
            "relationship": graph[concept][neighbor].get(
                "relationship", "related_to"
            )
        })

    return related


def save_graph():
    """Save the graph locally as JSON."""

    graph_path = Path(settings.KNOWLEDGE_GRAPH_PATH)
    graph_path.mkdir(parents=True, exist_ok=True)

    output_file = graph_path / "knowledge_graph.json"

    data = nx.node_link_data(graph)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    return str(output_file)


def load_graph():
    """Load the previously saved graph."""

    global graph

    graph_path = (
        Path(settings.KNOWLEDGE_GRAPH_PATH)
        / "knowledge_graph.json"
    )

    if graph_path.exists():
        with open(graph_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        graph = nx.node_link_graph(data, directed=True)

    return graph.number_of_nodes()


def remove_document_from_graph(document_id: str):
    """
    Remove one document's contributions.

    Concepts and relationships shared with other documents
    are preserved.
    """

    # Remove this document from relationship ownership
    edges_to_remove = []

    for source, target, attributes in list(graph.edges(data=True)):
        document_ids = attributes.get("document_ids", [])

        if document_id in document_ids:
            document_ids.remove(document_id)

        if not document_ids:
            # Preserve legacy edges that have no ownership metadata
            if "document_ids" in attributes:
                edges_to_remove.append((source, target))

    for source, target in edges_to_remove:
        graph.remove_edge(source, target)

    # Remove this document from concept ownership
    nodes_to_remove = []

    for concept, attributes in list(graph.nodes(data=True)):
        document_ids = attributes.get("document_ids", [])

        if document_id in document_ids:
            document_ids.remove(document_id)

        if (
            "document_ids" in attributes
            and not document_ids
            and graph.degree(concept) == 0
        ):
            nodes_to_remove.append(concept)

    for concept in nodes_to_remove:
        graph.remove_node(concept)

    save_graph()

    return {
        "removed_nodes": len(nodes_to_remove),
        "remaining_nodes": graph.number_of_nodes(),
        "remaining_relationships": graph.number_of_edges()
    }


def search_graph(question: str) -> list:
    """Find concepts and relationships relevant to a question."""

    from backend.app.graph.graph_extraction import CONCEPTS

    question_lower = question.lower()
    graph_results = []

    for concept in CONCEPTS:
        singular = concept.lower()

        plural_forms = [
            singular + "s",
            singular + "es"
        ]

        if singular in question_lower or any(
            word in question_lower for word in plural_forms
        ):
            if concept in graph:
                graph_results.append({
                    "concept": concept,
                    "related_concepts": get_related_concepts(concept)
                })

    return graph_results
