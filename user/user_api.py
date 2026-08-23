from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from core.security import create_access_token
from user.dependencies import get_current_user
from user.schemas import UserRegisterModel, EditUserModel, LoginModel
from user.userservice import register_user_db, edit_user_db, delete_user_db, \
                                check_user_existence_db, get_all_user_db, \
                                user_login_db

user_router = APIRouter(prefix='/user', tags=['Работа с пользователя'])

@user_router.get('/me')
async def get_me(current_user = Depends(get_current_user)):
    
    return {
        "user_id": current_user.user_id,
        "name": current_user.name,
        "surname": current_user.surname,
        "email": current_user.email,
    }

@user_router.get('/check_user')
async def check_existence(email: str, phone_number: str):
    return check_user_existence_db(email, phone_number)

@user_router.post('/register')
async def register_user(data: UserRegisterModel):
    new_user_data = data.model_dump()

    checker = check_user_existence_db(data.email, data.phone_number)
    
    if not checker:
        result = register_user_db(reg_date=datetime.now(), **new_user_data)

        return {'status': 1, 'message': result}

    return {'status': 0, 'message': checker}

@user_router.post('/login')
async def login(data: OAuth2PasswordRequestForm = Depends()):

    user = user_login_db(
            data.username,
            data.password
        )
    
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    

    access_token = create_access_token(
        user_id=user.user_id
    )

    return {
            "access_token": access_token,
            "token_type": "bearer"
        }

@user_router.get('/info')
async def get_user(current_user = Depends(get_current_user)):

    return {'status': 1, 'message': current_user}

@user_router.get('/get-all-users')
async def get_all_users():
    result = get_all_user_db()

    return result

@user_router.put('/edit-data')
async def edit_user(data: EditUserModel):
    change_data = data.model_dump()

    result = edit_user_db(**change_data)

    return {'status': 1, 'message': result}

@user_router.delete('/delete-user')
async def delete_user(user_id: int):
    result = delete_user_db(user_id)

    return {'status': 1, 'message': result}