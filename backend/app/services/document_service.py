
from pathlib import Path
import pymupdf  # PyMuPDF


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def validate_file(file_path: str) -> bool:
    """Check whether the uploaded file type is supported."""

    extension = Path(file_path).suffix.lower()

    return extension in SUPPORTED_EXTENSIONS


def extract_pdf_text(file_path: str) -> list:
    """Extract text from every page of a PDF."""

    pages = []

    document = pymupdf.open(file_path)

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page": page_number,
                    "text": text
                })
    finally:
        document.close()

    return pages


def extract_txt_text(file_path: str) -> list:
    """Extract text from a TXT file."""

    path = Path(file_path)

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    return [{
        "page": 1,
        "text": content.strip()
    }] if content.strip() else []


def process_document(file_path: str) -> dict:
    """Process a PDF or TXT document."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Document does not exist.")

    if not validate_file(file_path):
        raise ValueError("Only PDF and TXT files are supported.")

    extension = path.suffix.lower()

    if extension == ".pdf":
        pages = extract_pdf_text(file_path)
    else:
        pages = extract_txt_text(file_path)

    if not pages:
        raise ValueError(
            "No readable text found in the document."
        )

    return {
        "filename": path.name,
        "total_pages": len(pages),
        "pages": pages
    }
