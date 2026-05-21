from app.vectorstore.chroma_store import get_vector_store


def retrieve_context(
    user_id: int,
    query: str,
    collection_name: str = "General",
    k: int = 5
):
    vector_store = get_vector_store(user_id)

    docs = vector_store.similarity_search(
        query,
        k=k,
        filter={
            "collection_name": collection_name
        }
    )

    query_words = query.lower().split()

    scored_docs = []

    for doc in docs:
        content = (doc.page_content or "").strip()

        if not content:
            continue

        content_lower = content.lower()

        keyword_score = 0

        for word in query_words:
            if word in content_lower:
                keyword_score += 1

        scored_docs.append(
            (keyword_score, doc)
        )

    scored_docs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    context_parts = []
    sources = []

    for score, doc in scored_docs:
        content = doc.page_content.strip()

        context_parts.append(content)

        filename = doc.metadata.get("filename")

        if filename and filename not in sources:
            sources.append(filename)

    context = "\n\n".join(context_parts)

    return {
        "context": context,
        "sources": sources
    }