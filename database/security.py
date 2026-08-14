import os 

import jwt
from jwt.exceptions import InvalidTokenError

from user.userservice import get_exact_user_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
_hasher = PasswordHash.recommended()

class User(BaseModel):
    id: str
    email: str | None = None
    name: str | None = None
    surname: str | None = None

def hash_password(password: str) -> str:
    return _hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:  
    
    return _hasher.verify(
            plain_password,
            hashed_password
            )

def create_access_token(user_id: int) -> str:
    
    expire = datetime.now() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))

    payload = {
        "sub": str(user_id), 
        "exp": expire
    }

    return jwt.encode(
        payload, 
        SECRET_KEY,
        ALGORITHM
    )

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY, 
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None: 
            raise credentials_exception
        
        user_id = int(user_id)
    
    except (InvalidTokenError, ValueError): 
        raise credentials_exception
    
    user = get_exact_user_db(user_id)

    if user is None:
        raise credentials_exception
    
    return user