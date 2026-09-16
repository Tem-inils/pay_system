from decimal import Decimal

from pydantic import BaseModel


class CreateTransactionModel(BaseModel):
    account_from: str
    account_to: str
    amount: Decimal


class CancelTransactionModel(BaseModel):
    card_from: int
    card_to: int
    amount: float
    transfer_id: int