
from backend.app.services.chunking_service import chunk_documents

sample_pages = [
    {
        "page": 1,
        "text": (
            "Object-oriented programming is based on objects. "
            "A class is a blueprint for creating objects. "
            "Objects contain data and functions. "
        ) * 30
    },
    {
        "page": 2,
        "text": (
            "Inheritance allows one class to acquire properties "
            "of another class. "
        ) * 20
    }
]

chunks = chunk_documents(
    pages=sample_pages,
    chunk_size=800,
    chunk_overlap=150
)

print("Chunking successful!")
print("Total chunks:", len(chunks))

for index, chunk in enumerate(chunks[:3], start=1):
    print(f"\nChunk {index}")
    print("Page:", chunk["page"])
    print("Characters:", len(chunk["text"]))
    print("Text:", chunk["text"][:150])
