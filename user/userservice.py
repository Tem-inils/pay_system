from datetime import datetime

from database import get_db
from database.models import User
from sqlalchemy import or_
from sqlalchemy.orm import Session
from user.schemas import UserUpdate, ChangeUserPasswordModel
from core.security import hash_password, verify_password


def register_user_db(
            name: str,
            surname: str,
            email: str,
            phone_number: str,
            reg_date: datetime,
            password: str,
            city: str
        ) -> object:
    
    db = next(get_db())

    new_user = User(
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number,     
            reg_date=reg_date,
            hashed_password=hash_password(password),
            city=city
        )

    db.add(new_user)
    db.commit()

    return {
        "user_id": new_user.user_id,
        "name": new_user.name,
        "surname": new_user.surname, 
        "email": new_user.email,
        "phone_number": new_user.phone_number, 
        "city": new_user.city
    }

def user_login_db(email: str, password: str):
    db = next(get_db())

    user = db.query(User).filter_by(email=email).first()
    
    if not user: 
        return None
    
    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    
    return user

def user_change_password_db(db: Session, user: User, data: ChangeUserPasswordModel):

    if verify_password(data.current_password, user.hashed_password):
        user.hashed_password = hash_password(data.new_password)
        
        db.commit()
        db.refresh(user)

        return user
    else: 
        return None

def get_exact_user_db(
            user_id: int,
            db: Session
        ) -> User | None:

    exact_user = db.query(User).filter_by(user_id=user_id).first()

    return exact_user

def get_all_user_db() -> object:

    db = next(get_db())

    users = db.query(User).all()
    
    return users

def check_user_existence_db(email: str, phone_number: str) -> User | None:

    db = next(get_db())

    check_user = db.query(User).filter(
        or_(
            User.email == email,
            User.phone_number == phone_number,
        )
    ).first() 

    return check_user

def edit_user_db(
    db: Session,
    user: User,
    data: dict,
) -> User:


    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user
    
def delete_user_db(user_id: int) -> str:

    db = next(get_db())

    exact_user = db.query(User).filter_by(user_id=user_id).first()

    if exact_user:
        db.delete(exact_user)
        db.commit()

        return "User was removed"

    return "User not found"