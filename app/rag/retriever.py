from app.vectorstore.chroma_store import get_vector_store


def retrieve_context(user_id: int, query: str, k: int = 3):
    vector_store = get_vector_store(user_id)

    docs = vector_store.similarity_search(
        query,
        k=k
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context