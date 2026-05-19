from sqlalchemy.orm import Session
from app.models.uploaded_document import UploadedDocument


def save_uploaded_document(
    db: Session,
    user_id: int,
    filename: str,
    document_text: str
):
    doc = UploadedDocument(
        user_id=user_id,
        filename=filename,
        document_text=document_text
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    return doc


def get_uploaded_documents(
    db: Session,
    user_id: int
):
    return db.query(UploadedDocument).filter(
        UploadedDocument.user_id == user_id
    ).order_by(
        UploadedDocument.created_at.desc()
    ).all()

def delete_uploaded_document(
    db: Session,
    document_id: int,
    user_id: int
):
    doc = db.query(UploadedDocument).filter(
        UploadedDocument.id == document_id,
        UploadedDocument.user_id == user_id
    ).first()

    if not doc:
        return None

    db.delete(doc)
    db.commit()

    return doc