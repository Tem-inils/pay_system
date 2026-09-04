import os 

import jwt
from jwt.exceptions import InvalidTokenError

from pydantic import BaseModel
from datetime import datetime, timedelta
from pwdlib import PasswordHash

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
SECRET_KEY = os.getenv("SECRET_KEY")

if SECRET_KEY is None:
    raise RuntimeError("SECRET_KEY is not set")

_hasher = PasswordHash.recommended()

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

def decode_access_token(token: str) -> int | None:
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY, 
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None: 
            return None
        
        return int(user_id)
            
    except (InvalidTokenError, ValueError): 
        return None
    
