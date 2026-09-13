from pydantic import BaseModel

class CreateAccountModel(BaseModel):
    user_id: int
    currenccy: str

