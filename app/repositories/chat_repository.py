from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory


def save_chat(
    db: Session,
    user_id: int,
    message: str,
    response: str
):
    chat = ChatHistory(
        user_id=user_id,
        message=message,
        response=response
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_user_chat_history(
    db: Session,
    user_id: int
):
    return db.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(
        ChatHistory.created_at.desc()
    ).all()