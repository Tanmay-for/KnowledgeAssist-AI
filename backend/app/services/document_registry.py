
import json
from datetime import datetime
from pathlib import Path

from backend.app.core.config import settings


REGISTRY_PATH = settings.CHROMA_DB_PATH.parent / "documents.json"


def load_documents():
    """Load the saved document registry."""
    if not REGISTRY_PATH.exists():
        return []

    try:
        with open(REGISTRY_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_documents(documents):
    """Save document information permanently."""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

    temp_path = REGISTRY_PATH.with_suffix(".tmp")

    with open(temp_path, "w", encoding="utf-8") as file:
        json.dump(documents, file, indent=4)

    temp_path.replace(REGISTRY_PATH)


def register_document(document_info):
    """Add a newly uploaded document to the registry."""
    documents = load_documents()

    document_info["upload_date"] = datetime.now().isoformat(
        timespec="seconds"
    )

    documents.append(document_info)
    save_documents(documents)

    return document_info
