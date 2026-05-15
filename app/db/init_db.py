from app.db.database import Base
from app.db.database import engine

from app.models.user import User
from app.models.chat_history import ChatHistory
from app.models.generated_output import GeneratedOutput
from app.models.ats_report import ATSReport
from app.models.uploaded_document import UploadedDocument


def init_database():
    Base.metadata.create_all(bind=engine)