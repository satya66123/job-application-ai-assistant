from app.rag.chunker import chunk_document
from app.vectorstore.chroma_store import get_vector_store


def ingest_document(text: str, user_id: int):
    chunks = chunk_document(text)

    print("CHUNKS:", chunks)

    vector_store = get_vector_store(user_id)

    vector_store.add_texts(chunks)

    return len(chunks)