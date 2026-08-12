from fastapi import APIRouter
from datetime import datetime

from database.userservice import register_user_db, edit_user_db, delete_user_db, \
                                get_exact_user_db, check_user_existence_db, get_all_user_db, \
                                user_login_db

from user import UserRegisterModel, EditUserModel, LoginSchema

user_router = APIRouter(prefix='/user', tags=['Работа с пользователя'])


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
async def login(data: LoginSchema):

    user = user_login_db(data.email, data.password)

    return {"status": 0, "message": user}

@user_router.get('/info')
async def get_user(user_id: int):
    result = get_exact_user_db(user_id)

    return {'status': 1 if result else 0, 'message': result}

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