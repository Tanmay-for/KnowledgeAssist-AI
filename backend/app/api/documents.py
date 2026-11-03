
from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.services.document_registry import (
    load_documents,
    save_documents
)

from backend.app.rag.vector_store import collection

from backend.app.graph.knowledge_graph import (
    load_graph,
    remove_document_from_graph
)


router = APIRouter(
    prefix="/documents",
    tags=["Document Management"]
)


@router.get("/")
def get_documents():
    """Get all uploaded documents."""

    documents = load_documents()

    return {
        "status": "success",
        "total_documents": len(documents),
        "documents": documents
    }


@router.delete("/{document_id}")
def delete_document(document_id: str):
    """Delete a document and its associated data."""

    documents = load_documents()

    # Find document in registry
    document = next(
        (
            item for item in documents
            if item.get("document_id") == document_id
        ),
        None
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    file_path = Path(document.get("file_path", ""))

    try:
        # 1. Delete document chunks from ChromaDB
        collection.delete(
            where={"document_id": document_id}
        )

        # 2. Remove document contributions from Knowledge Graph
        load_graph()
        graph_result = remove_document_from_graph(document_id)

        # 3. Delete uploaded file
        if file_path.exists():
            file_path.unlink()

        # 4. Remove document from registry
        updated_documents = [
            item for item in documents
            if item.get("document_id") != document_id
        ]

        save_documents(updated_documents)

        return {
            "status": "success",
            "message": "Document deleted successfully.",
            "deleted_document": document.get(
                "original_filename"
            ),
            "document_id": document_id,
            "knowledge_graph": graph_result
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document deletion failed: {error}"
        )
