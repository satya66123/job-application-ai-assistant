from app.rag.chunker import chunk_document
from app.vectorstore.chroma_store import get_vector_store


def ingest_document(
    text: str,
    user_id: int,
    filename: str
):
    chunks = chunk_document(text)

    vector_store = get_vector_store(user_id)

    metadatas = []

    for _ in chunks:
        metadatas.append({
            "filename": filename,
            "user_id": user_id
        })

    vector_store.add_texts(
        texts=chunks,
        metadatas=metadatas
    )

    return len(chunks)