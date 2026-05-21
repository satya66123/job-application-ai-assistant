from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repositories.admin_repository import get_dashboard_stats

from app.db.database import get_db
from app.auth.dependencies import get_current_user

from app.rag.ingestion import ingest_document
from app.rag.retriever import retrieve_context
from app.vectorstore.chroma_store import delete_vectors_by_filename

from app.prompts.prompts import RAG_CHAT_PROMPT
from app.services.openai_service import generate_resume_content
from app.repositories.document_repository import rename_uploaded_document

from app.repositories.document_repository import document_exists

from app.repositories.document_repository import (
    save_uploaded_document,
    get_uploaded_documents,
    delete_uploaded_document
)

from app.repositories.document_repository import delete_collection_documents
from app.vectorstore.chroma_store import delete_vectors_by_collection

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

security = HTTPBearer()


# ---------------- REQUEST MODELS ----------------

class KnowledgeUploadRequest(BaseModel):
    filename: str
    document_text: str
    collection_name: str = "General"

class RenameDocumentRequest(BaseModel):
    new_filename: str

class RAGChatRequest(BaseModel):
    question: str
    modelName: str
    collection_name: str = "General"
    chat_history: list = []
# ---------------- UPLOAD KNOWLEDGE ----------------

@router.post("/upload-knowledge")
def upload_knowledge(
    data: KnowledgeUploadRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    if document_exists(
            db=db,
            user_id=user.id,
            filename=data.filename
    ):
        return {
            "error": "Document with same filename already uploaded."
        }

    chunk_count = ingest_document(
        data.document_text,
        user.id,
        data.filename,
        data.collection_name
    )

    save_uploaded_document(
        db=db,
        user_id=user.id,
        filename=data.filename,
        document_text=data.document_text,
        collection_name=data.collection_name
    )

    return {
        "message": "Knowledge uploaded successfully",
        "chunks_created": chunk_count,
        "user_id": user.id
    }


# ---------------- RAG CHAT ----------------

@router.post("/chat")
def rag_chat(
    data: RAGChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    retrieval_result = retrieve_context(
        user.id,
        data.question,
        data.collection_name
    )

    context = retrieval_result.get("context", "")
    sources = retrieval_result.get("sources", [])

    print("RAG CONTEXT:", repr(context))
    print("SOURCES:", sources)
    print("QUESTION:", data.question)

    if not context:
        return {
            "answer": "I could not find that in uploaded knowledge.",
            "sources": [],
            "user_id": user.id
        }

    history_text = ""

    for message in data.chat_history[-6:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        history_text += f"{role}: {content}\n"

    full_question = f"""
Previous conversation:
{history_text}

Current question:
{data.question}
"""

    prompt = RAG_CHAT_PROMPT.format(
        context=context,
        question=full_question
    )

    result = generate_resume_content(
        prompt,
        data.modelName
    )

    if not result["success"]:
        return {
            "error": result["error"],
            "sources": []
        }

    answer = result["response"]
    fallback = "I could not find"

    if "could not find" in answer.casefold():
        return {
            "answer": answer,
            "sources": [],
            "user_id": user.id
        }

    return {
        "answer": answer,
        "sources": sources,
        "user_id": user.id
    }

# ---------------- LIST DOCUMENTS ----------------

@router.get("/documents")
def list_uploaded_documents(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    docs = get_uploaded_documents(
        db=db,
        user_id=user.id
    )

    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "created_at": doc.created_at
        }
        for doc in docs
    ]


# ---------------- DELETE DOCUMENT ----------------

@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    deleted_doc = delete_uploaded_document(
        db=db,
        document_id=document_id,
        user_id=user.id
    )

    if not deleted_doc:
        return {
            "error": "Document not found"
        }

    delete_vectors_by_filename(
        user.id,
        deleted_doc.filename
    )

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }

@router.delete("/collections/{collection_name}")
def delete_collection(
    collection_name: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    deleted_docs = delete_collection_documents(
        db=db,
        user_id=user.id,
        collection_name=collection_name
    )

    if not deleted_docs:
        return {
            "error": "Collection not found"
        }

    delete_vectors_by_collection(
        user.id,
        collection_name
    )

    return {
        "message": f"{collection_name} collection deleted successfully",
        "deleted_count": len(deleted_docs)
    }


@router.put("/documents/{document_id}/rename")
def rename_document(
    document_id: int,
    data: RenameDocumentRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    renamed_doc = rename_uploaded_document(
        db=db,
        document_id=document_id,
        user_id=user.id,
        new_filename=data.new_filename
    )

    if not renamed_doc:
        return {
            "error": "Document not found"
        }

    return {
        "message": "Document renamed successfully",
        "document_id": renamed_doc.id,
        "new_filename": renamed_doc.filename
    }

@router.get("/admin/dashboard")
def admin_dashboard(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    stats = get_dashboard_stats(db)

    return stats