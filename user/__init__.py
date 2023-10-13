from pydantic import BaseModel


# Класс валидации для регистрации
class UserRegisterModel(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    password: str
    city: str


# Класс валидации для изменения данных пользователя
class EditUserModel(BaseModel):
    user_id: int
    edit_type: str
    new_data: str