from pydantic import BaseModel


# Класс для валидации создания перевода
class CreateTransactionModel(BaseModel):
    card_from: int
    card_to: int
    amount: float


# Класс для валидации отмены перевода
class CancelTransactionModel(BaseModel):
    card_from: int
    card_to: int
    amount: float
    transfer_id: int