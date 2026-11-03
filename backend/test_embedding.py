
from backend.app.services.embedding_service import generate_embedding

sample_text = "A class is a blueprint for creating objects in C++."

try:
    vector = generate_embedding(sample_text)

    print("Embedding generated successfully!")
    print("Vector dimensions:", len(vector))
    print("First 5 values:", vector[:5])

except Exception as error:
    print("Error:", error)
