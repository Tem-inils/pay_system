from datetime import datetime

from database.models import User
from sqlalchemy import or_
from sqlalchemy.orm import Session
from user.schemas import UserRegisterModel, UserUpdateModel, ChangeUserPasswordModel
from core.security import hash_password, verify_password


def register_user_db(
            data: UserRegisterModel,
            db: Session,
        ) -> object:
    

    new_user = User(
            name=data.name,
            surname=data.surname,
            email=data.email,
            phone_number=data.phone_number,     
            reg_date=datetime.now(),
            hashed_password=hash_password(data.password),
            city=data.city
        )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def user_login_db(email: str, password: str, db: Session):
    

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

        return True
    else: 
        return False 

def get_exact_user_db(
            user_id: int,
            db: Session
        ) -> User | None:

    exact_user = db.query(User).filter_by(id=user_id).first()

    return exact_user

def check_user_existence_db(email: str, phone_number: str, db: Session) -> User | None:

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
    
def delete_user_db(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.commit()