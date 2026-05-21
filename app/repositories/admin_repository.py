from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.uploaded_document import UploadedDocument


def get_dashboard_stats(db: Session):
    total_users = db.query(User).count()

    total_documents = db.query(UploadedDocument).count()

    collections = db.query(
        UploadedDocument.collection_name,
        func.count(UploadedDocument.id)
    ).group_by(
        UploadedDocument.collection_name
    ).all()

    collection_stats = []

    for name, count in collections:
        collection_stats.append({
            "collection_name": name,
            "document_count": count
        })

    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "collections": collection_stats
    }