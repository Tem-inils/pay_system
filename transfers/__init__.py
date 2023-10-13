from pydantic import BaseModel

class CreateTransactionModel(BaseModel):
    card_from: int
    card_to: int
    amount: float

class CancelTransactionModel(BaseModel):
    card_from: int
    card_to: int
    amount: float
    transfer_id: int