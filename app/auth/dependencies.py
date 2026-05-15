from jose import JWTError
from jose import jwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.auth.auth_utils import SECRET_KEY
from app.auth.auth_utils import ALGORITHM


def get_current_user(
    token: str,
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_email = payload.get("sub")

        if user_email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(
        User.email == user_email
    ).first()

    if user is None:
        raise credentials_exception

    return user