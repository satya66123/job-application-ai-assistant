from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Text
from datetime import datetime

from app.db.database import Base


class ATSReport(Base):
    __tablename__ = "ats_reports"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    resume_text = Column(Text)

    job_description = Column(Text)

    match_score = Column(String(50))

    report = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )