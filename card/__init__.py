from pydantic import BaseModel

class CardAddModel(BaseModel):
    user_id: int
    card_number: int
    balance: float
    card_name: str
    exp_date: int
    cvv: int

class EditCardModel(BaseModel):
    id: int
    design_path: str