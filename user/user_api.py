"""FastAPI"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

"""DataBase"""
from sqlalchemy.orm import Session
from database import get_db
from database.models import User

from datetime import datetime
from core.security import create_access_token

"""User imports"""
from user.dependencies import get_current_user
from user.schemas import UserRegisterModel, UserUpdateModel, UserResponse, UserLoginModel, ChangeUserPasswordModel
from user.userservice import register_user_db, edit_user_db, check_user_existence_db, \
    user_login_db, user_change_password_db, delete_user_db

user_router = APIRouter(prefix='/user', tags=['User API'])

"""Register & Login"""


@user_router.post('/register', response_model=UserResponse, status_code=201)
async def register_user(data: UserRegisterModel, db: Session = Depends(get_db)):
    checker = check_user_existence_db(data.email, data.phone_number, db)

    if checker:
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    result = register_user_db(
        db=db,
        data=data,
    )

    return result


@user_router.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_login_db(
        data.username,
        data.password,
        db,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        user_id=user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


""" User Function """


@user_router.get('/me', response_model=UserResponse, )
async def get_me(current_user=Depends(get_current_user), ):
    return current_user


@user_router.patch('/me', response_model=UserResponse, )
def update_me(data: UserUpdateModel, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), ):
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    if "email" in update_data:
        existing_user = (
            db.query(User)
            .filter(
                User.email == update_data["email"],
                User.id != current_user.id,
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email is already in use",
            )

    if "phone_number" in update_data:
        existing_user = (
            db.query(User)
            .filter(
                User.phone_number == update_data["phone_number"],
                User.id != current_user.id,
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Phone number is already in use",
            )

    updated_user = edit_user_db(
        db=db,
        user=current_user,
        data=update_data,
    )

    return updated_user


@user_router.delete("/me", status_code=204, )
def delete_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), ):
    delete_user_db(
        db=db,
        user=current_user,
    )


@user_router.patch('/password')
def change_password(data: ChangeUserPasswordModel,
                    current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    result = user_change_password_db(db, current_user, data)

    if result:
        return {"message": "Password has been changed"}
    else:
        raise HTTPException(
            status_code=409,
            detail="Inncorects password",
        )
