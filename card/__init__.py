from pydantic import BaseModel

# класс для валидации добовления карты

class CardAddModel(BaseModel):
    user_id: int
    card_number: int
    balance: float
    card_name: str
    exp_date: int
    cvv: int



# Класс для валидации извенения
class EditCardModel(BaseModel):
    card_id: int
    design_path: str
