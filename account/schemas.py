from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from database.models import AccountCurrency


class CreateAccountModel(BaseModel):
    currency: AccountCurrency

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "currency": "USD"
            }
        }
    )


class UpdateAccountModel(BaseModel):
    pass


class AccountResponseModel(BaseModel):
    account_number: str
    currency: str
    balance: Decimal
    is_active: bool


