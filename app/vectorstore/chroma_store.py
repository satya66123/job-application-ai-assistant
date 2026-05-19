from langchain_chroma import Chroma
from app.rag.embeddings import get_embeddings


def get_vector_store(user_id: int):
    return Chroma(
        persist_directory=f"./chroma_db/user_{user_id}",
        embedding_function=get_embeddings()
    )


def delete_vectors_by_filename(
    user_id: int,
    filename: str
):
    vector_store = get_vector_store(user_id)

    vector_store.delete(
        where={
            "filename": filename
        }
    )