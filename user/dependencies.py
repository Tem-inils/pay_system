from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from database.models import User
from database import get_db
from core.security import decode_access_token
from user.userservice import get_exact_user_db


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db), 
) -> User:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    user_id = decode_access_token(token)

    if user_id is None:
        raise credentials_exception

    user = get_exact_user_db(user_id, db)

    if user is None:
        raise credentials_exception

    return user