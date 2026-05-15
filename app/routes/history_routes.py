from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.auth.dependencies import get_current_user

from app.repositories.chat_repository import get_user_chat_history
from app.repositories.output_repository import get_user_outputs
from app.repositories.ats_repository import get_user_ats_reports

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

security = HTTPBearer()


@router.get("/chat")
def chat_history(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    history = get_user_chat_history(
        db,
        user.id
    )

    return history


@router.get("/outputs")
def generated_outputs(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    outputs = get_user_outputs(
        db,
        user.id
    )

    return outputs


@router.get("/ats")
def ats_history(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user = get_current_user(
        token=token,
        db=db
    )

    reports = get_user_ats_reports(
        db,
        user.id
    )

    return reports