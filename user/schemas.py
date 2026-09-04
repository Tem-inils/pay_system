from pydantic import BaseModel, EmailStr

class UserUpdate(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    city: str | None = None
    password: str | None = None

class UserRegisterModel(BaseModel):
    name: str
    surname: str
    email: EmailStr 
    phone_number: str
    password: str
    city: str

class UserLoginModel(BaseModel):
    email: EmailStr 
    password: str

class UserResponse(BaseModel):
    user_id: int
    name: str
    surname: str
    email: str
    phone_number: str
    city: str

    class Config:
        from_attributes = True

