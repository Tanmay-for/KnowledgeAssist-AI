
def chunk_documents(
    pages: list,
    chunk_size: int = 800,
    chunk_overlap: int = 150
) -> list:
    """
    Divide extracted document pages into smaller chunks.
    Preserve the original page number for citations.
    """

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Overlap must be non-negative and smaller than chunk size."
        )

    chunks = []
    step = chunk_size - chunk_overlap

    for page in pages:
        text = page["text"].strip()
        page_number = page["page"]

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            start += step

    return chunks
