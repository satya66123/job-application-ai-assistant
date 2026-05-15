from app.db.database import engine
from app.models.user import User
from app.db.database import Base


def init_database():
    Base.metadata.create_all(bind=engine)