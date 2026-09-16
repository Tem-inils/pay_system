import secrets
import string
from enum import Enum


class AccountCurrency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    TRL = "TRL"


def generate_account_number():
    digits = "".join(
        secrets.choice(string.digits) for _ in range(16)
    )

    return f"ACC-{digits}"
