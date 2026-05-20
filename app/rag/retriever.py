from app.vectorstore.chroma_store import get_vector_store


def retrieve_context(
    user_id: int,
    query: str,
    collection_name: str = "General",
    k: int = 3
):
    vector_store = get_vector_store(user_id)

    docs = vector_store.similarity_search(
        query,
        k=k,
        filter={
            "collection_name": collection_name
        }
    )

    context_parts = []
    sources = []

    for doc in docs:
        content = (doc.page_content or "").strip()

        # ONLY keep docs with real content
        if not content:
            continue

        context_parts.append(content)

        filename = doc.metadata.get("filename")

        if  filename and filename not in sources:
            sources.append(filename)

    context = "\n\n".join(context_parts)

    return {
        "context": context,
        "sources": sources
    }