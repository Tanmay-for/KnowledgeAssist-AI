
import chromadb

from backend.app.core.config import settings


# Create a persistent local ChromaDB database
client = chromadb.PersistentClient(
    path=str(settings.CHROMA_DB_PATH)
)


# Create or access our document collection
collection = client.get_or_create_collection(
    name="knowledgeassist_documents",
    metadata={"hnsw:space": "cosine"}
)


def add_documents(
    texts: list,
    embeddings: list,
    metadatas: list,
    ids: list
):
    """Store document chunks and embeddings in ChromaDB."""

    if not (
        len(texts) == len(embeddings)
        == len(metadatas) == len(ids)
    ):
        raise ValueError("All input lists must have equal lengths.")

    if not texts:
        raise ValueError("No documents provided.")

    collection.upsert(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )

    return len(texts)


def search_documents(query_embedding: list, top_k: int = 5):
    """Find the most relevant document chunks."""

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    return results


def get_document_count():
    """Return the number of stored document chunks."""

    return collection.count()
def delete_test_documents():
    results = collection.get(
        where={"filename": "sample.txt"},
        include=["metadatas"]
    )

    ids = results.get("ids", [])

    if ids:
        collection.delete(ids=ids)
        return len(ids)

    return 0