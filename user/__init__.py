from pydantic import BaseModel

class UserRegisterModel(BaseModel):
    name: str
    sutname: str
    email: str
    phone_number: str
    password: str
    city: str


class EditUserModel(BaseModel):
    user_id: int
    edit_type: str
    new_data: str