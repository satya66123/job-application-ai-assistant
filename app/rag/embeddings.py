from langchain_ollama import OllamaEmbeddings

embedding_model = OllamaEmbeddings(
    model="nomic-embed-text:latest"
)


def get_embeddings():
    return embedding_model