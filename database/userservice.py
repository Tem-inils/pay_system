from datetime import datetime

from database.models import User
from database import get_db
from database.security import hash_password, verify_password


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

    return new_user

def user_login_db(email: str, password: str):
    db = next(get_db())

    user = db.query(User).filter_by(email=email).first()
    
    if user:
        password_checker = verify_password(plain_password=password, hashed_password=user.hashed_password)
        
        if password_checker:
            return user
        
    
    return "Incorrect email addres or password"

def get_exact_user_db(user_id: int) -> object:

    db = next(get_db())

    exact_user = db.query(User).filter_by(user_id=user_id).first()

    return exact_user

def get_all_user_db() -> object:

    db = next(get_db())

    users = db.query(User).all()
    
    return users

def check_user_existence_db(email: str, phone_number: str):

    db = next(get_db())

    check_user_email = db.query(User).filter_by(email=email).first() 
    if check_user_email: 
        return "This email adress has already been used"
    
    check_user_number = db.query(User).filter_by(phone_number=phone_number).first()
    if check_user_number:
        return "This phone number has already been used"

def edit_user_db(user_id: int, edit_type: str, new_data: str):

    db = next(get_db())

    user = db.query(User).filter_by(user_id=user_id).first()

    if user:
        if edit_type == 'email':
            user.email = new_data

        elif edit_type == 'password':
            user.hashed_password = new_data

        elif edit_type == 'city':
            user.city = new_data

        db.commit()

def delete_user_db(user_id: int) -> str:

    db = next(get_db())

    exact_user = db.query(User).filter_by(user_id=user_id).first()

    if exact_user:
        db.delete(exact_user)
        db.commit()

        return "User was removed"

    return "User not found"