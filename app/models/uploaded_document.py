from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from datetime import datetime

from app.db.database import Base


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    filename = Column(String(255))

    collection_name = Column(
        String(100),
        default="General"
    )

    document_text = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )