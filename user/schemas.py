from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserUpdateModel(BaseModel):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    city: str | None = None

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Rafael",
                "city": "Tashkent"
            }
        }
    )

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

class ChangeUserPasswordModel(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

    model_config = ConfigDict(
        extra="forbid",
    )

class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    phone_number: str
    city: str

    class Config:
        from_attributes = True

