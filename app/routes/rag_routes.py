from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.dependencies import get_current_user

from app.rag.ingestion import ingest_document
from app.rag.retriever import retrieve_context
from app.vectorstore.chroma_store import delete_vectors_by_filename

from app.prompts.prompts import RAG_CHAT_PROMPT
from app.services.openai_service import generate_resume_content

from app.repositories.document_repository import (
    save_uploaded_document,
    get_uploaded_documents,
    delete_uploaded_document
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

security = HTTPBearer()


# ---------------- REQUEST MODELS ----------------

class KnowledgeUploadRequest(BaseModel):
    filename: str
    document_text: str


class RAGChatRequest(BaseModel):
    question: str
    modelName: str
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

    chunk_count = ingest_document(
        data.document_text,
        user.id,
        data.filename
    )

    save_uploaded_document(
        db=db,
        user_id=user.id,
        filename=data.filename,
        document_text=data.document_text
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

    context = retrieve_context(
        user.id,
        data.question
    )

    print("RAG CONTEXT:")
    print(repr(context))

    print("QUESTION:")
    print(data.question)

    if not context or not context.strip():
        return {
            "answer": "I could not find that in uploaded knowledge.",
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
            "error": result["error"]
        }

    return {
        "answer": result["response"],
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