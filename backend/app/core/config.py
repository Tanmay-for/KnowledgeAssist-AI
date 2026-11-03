import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[3]

# Load environment variables from the project root
load_dotenv(BASE_DIR / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "KnowledgeAssist AI")

    OLLAMA_BASE_URL = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )

    LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:3b")

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL", "nomic-embed-text"
    )

    CHROMA_DB_PATH = BASE_DIR / os.getenv(
        "CHROMA_DB_PATH", "data/chroma_db"
    )

    KNOWLEDGE_GRAPH_PATH = BASE_DIR / os.getenv(
        "KNOWLEDGE_GRAPH_PATH", "data/knowledge_graph"
    )

    UPLOAD_TEMP_PATH = BASE_DIR / os.getenv(
        "UPLOAD_TEMP_PATH", "data/uploads/temporary"
    )

    UPLOAD_PERMANENT_PATH = BASE_DIR / os.getenv(
        "UPLOAD_PERMANENT_PATH", "data/uploads/permanent"
    )


settings = Settings()