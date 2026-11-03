
from backend.app.graph.graph_extraction import build_graph_from_text
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import uuid

from backend.app.core.config import settings
from backend.app.services.document_service import process_document
from backend.app.services.chunking_service import chunk_documents
from backend.app.services.embedding_service import generate_embeddings
from backend.app.rag.vector_store import add_documents
from backend.app.services.document_registry import register_document


router = APIRouter(prefix="/upload", tags=["Document Upload"])

MAX_FILE_SIZE = 20 * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".txt"}


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    storage_type: str = Form(...)
):
    if storage_type not in {"temporary", "permanent"}:
        raise HTTPException(
            status_code=400,
            detail="Storage type must be temporary or permanent."
        )

    original_filename = file.filename or "Unknown"
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported."
        )

    storage_path = (
        settings.UPLOAD_TEMP_PATH
        if storage_type == "temporary"
        else settings.UPLOAD_PERMANENT_PATH
    )

    storage_path.mkdir(parents=True, exist_ok=True)

    document_id = str(uuid.uuid4())
    safe_filename = f"{document_id}{extension}"
    file_path = storage_path / safe_filename

    chunk_ids = []
    vector_records_added = False

    try:
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds the 20 MB limit."
            )

        file_path.write_bytes(content)

        # Step 1: Extract text
        result = process_document(str(file_path))

        # Step 2: Build Knowledge Graph
        full_text = "\n".join(
            page["text"] for page in result["pages"]
        )

        graph_result = build_graph_from_text(full_text, document_id)

        # Step 3: Divide text into chunks
        chunks = chunk_documents(result["pages"])

        if not chunks:
            raise ValueError("No text chunks could be generated.")

        # Step 4: Generate embeddings
        chunk_texts = [
            chunk["text"] for chunk in chunks
        ]

        embeddings = generate_embeddings(chunk_texts)

        # Step 5: Prepare metadata
        metadatas = [
            {
                "document_id": document_id,
                "filename": original_filename,
                "page": chunk["page"],
                "storage_type": storage_type
            }
            for chunk in chunks
        ]

        # Step 6: Generate unique chunk IDs
        chunk_ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        # Step 7: Store in ChromaDB
        stored_count = add_documents(
            texts=chunk_texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=chunk_ids
        )

        vector_records_added = True

        # Step 8: Save document details in JSON registry
        register_document({
            "document_id": document_id,
            "original_filename": original_filename,
            "storage_type": storage_type,
            "total_pages": result["total_pages"],
            "total_chunks": stored_count,
            "file_path": str(file_path),
            "status": "success"
        })

        return {
            "message": "Document uploaded and indexed successfully.",
            "document_id": document_id,
            "original_filename": original_filename,
            "storage_type": storage_type,
            "total_pages": result["total_pages"],
            "total_chunks": stored_count,
            "vector_database": "ChromaDB",
            "status": "success",
            "graph_concepts": len(graph_result["concepts"]),
            "graph_relationships": len(graph_result["relationships"])
        }

    except HTTPException:
        if vector_records_added and chunk_ids:
            from backend.app.rag.vector_store import collection
            collection.delete(ids=chunk_ids)

        file_path.unlink(missing_ok=True)
        raise

    except Exception as error:
        if vector_records_added and chunk_ids:
            try:
                from backend.app.rag.vector_store import collection
                collection.delete(ids=chunk_ids)
            except Exception:
                pass

        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {error}"
        )

    finally:
        await file.close()
