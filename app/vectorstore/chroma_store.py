from langchain_chroma import Chroma
from app.rag.embeddings import get_embeddings


def get_vector_store(user_id: int):
    return Chroma(
        persist_directory=f"./chroma_db/user_{user_id}",
        embedding_function=get_embeddings()
    )