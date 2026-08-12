from pwdlib import PasswordHash

_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return _hasher.hash(password)

def verify_password(
            plain_password: str,
            hashed_password: str
        ) -> bool:  
    
    return _hasher.verify(
            plain_password,
            hashed_password
            )