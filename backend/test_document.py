
from backend.app.services.document_service import process_document


file_path = "test_documents/notes.pdf"

try:
    result = process_document(file_path)

    print("\nDocument processed successfully!")
    print("Filename:", result["filename"])
    print("Pages:", result["total_pages"])

    print("\nExtracted text:")
    for page in result["pages"]:
        print(page["text"])

except Exception as error:
    print("Error:", error)
