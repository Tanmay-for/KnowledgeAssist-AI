
from backend.app.rag.vector_store import (
    add_documents,
    search_documents,
    get_document_count
)

from backend.app.services.embedding_service import generate_embedding


text = "A class is a blueprint for creating objects in C++."

try:
    embedding = generate_embedding(text)

    add_documents(
        texts=[text],
        embeddings=[embedding],
        metadatas=[{
            "filename": "sample.txt",
            "page": 1
        }],
        ids=["test-document-001"]
    )

    print("Document stored successfully!")
    print("Total documents:", get_document_count())

    query = "What is a class in C++?"
    query_embedding = generate_embedding(query)

    results = search_documents(query_embedding)

    print("\nSearch Results:")
    print(results["documents"])

except Exception as error:
    print("Error:", error)
