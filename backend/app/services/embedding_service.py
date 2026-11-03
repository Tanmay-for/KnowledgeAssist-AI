
import ollama

from backend.app.core.config import settings


def generate_embedding(text: str) -> list:
    """
    Convert text into a numerical vector
    using the local Ollama embedding model.
    """

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        response = ollama.embed(
            model=settings.EMBEDDING_MODEL,
            input=text
        )

        return response["embeddings"][0]

    except Exception as error:
        raise RuntimeError(
            f"Embedding generation failed: {error}"
        )


def generate_embeddings(texts: list) -> list:
    """
    Generate embeddings for multiple text sections.
    """

    embeddings = []

    for text in texts:
        embedding = generate_embedding(text)
        embeddings.append(embedding)

    return embeddings
