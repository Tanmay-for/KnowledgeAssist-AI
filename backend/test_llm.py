
from backend.app.services.llm_service import generate_response


prompt = """
Explain object-oriented programming in simple language.
Give a short example using C++.
"""


try:
    print("Generating response using Ollama...\n")

    answer = generate_response(prompt)

    print("LLM Response:")
    print("=" * 50)
    print(answer)

    print("\nLLM test completed successfully!")

except Exception as error:
    print("Error:", error)
