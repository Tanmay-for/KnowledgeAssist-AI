
from backend.app.services.embedding_service import generate_embedding
from backend.app.rag.vector_store import search_documents


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 5
) -> list:
    """Retrieve relevant document chunks for a question."""

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be positive.")

    query_embedding = generate_embedding(question)

    results = search_documents(
        query_embedding=query_embedding,
        top_k=top_k
    )

    retrieved_chunks = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        retrieved_chunks.append({
            "text": document,
            "filename": metadata.get("filename", "Unknown"),
            "page": metadata.get("page", "Unknown"),
            "distance": distance
        })

    return retrieved_chunks
