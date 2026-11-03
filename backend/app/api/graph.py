from fastapi import APIRouter, HTTPException

from backend.app.graph import knowledge_graph

router = APIRouter(
    prefix="/graph",
    tags=["Knowledge Graph"]
)


@router.get("/")
def get_knowledge_graph():

    try:
        # Load saved knowledge graph
        knowledge_graph.load_graph()

        # Get NetworkX graph
        graph = knowledge_graph.graph

        # Convert nodes into JSON format
        nodes = []

        for node, attributes in graph.nodes(data=True):
            nodes.append({
                "id": str(node),
                "label": str(node),
                "type": attributes.get("type", "Concept")
            })

        # Convert relationships into JSON format
        edges = []

        for source, target, attributes in graph.edges(data=True):
            edges.append({
                "source": str(source),
                "target": str(target),
                "relationship": attributes.get(
                    "relationship",
                    "related_to"
                )
            })

        return {
            "status": "success",
            "total_nodes": len(nodes),
            "total_relationships": len(edges),
            "nodes": nodes,
            "edges": edges
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve knowledge graph: {error}"
        )