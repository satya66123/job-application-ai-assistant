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

from app.prompts.prompts import RAG_CHAT_PROMPT
from app.services.openai_service import generate_resume_content
from app.repositories.document_repository import save_uploaded_document
from app.repositories.document_repository import get_uploaded_documents

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

security = HTTPBearer()


class KnowledgeUploadRequest(BaseModel):
    filename: str
    document_text: str

class RAGChatRequest(BaseModel):
    question: str
    modelName: str


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
        user.id
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

    prompt = RAG_CHAT_PROMPT.format(
        context=context,
        question=data.question
    )

    context = retrieve_context(
        user.id,
        data.question
    )

    print("RAG CONTEXT:")
    print(context)
    print("QUESTION:")
    print(data.question)
    result = generate_resume_content(
        prompt,
        data.modelName
    )

    if not result["success"]:
        return {"error": result["error"]}

    return {
        "answer": result["response"],
        "user_id": user.id
    }
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