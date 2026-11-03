
import ollama

from backend.app.core.config import settings


# Connect to the local Ollama server
client = ollama.Client(
    host=settings.OLLAMA_BASE_URL
)


def generate_response(prompt: str) -> str:
    """
    Generate an answer using the local Qwen model.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    try:
        response = client.chat(
            model=settings.LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.3
            }
        )

        return response["message"]["content"]

    except Exception as error:
        raise RuntimeError(
            f"LLM response generation failed: {error}"
        )
