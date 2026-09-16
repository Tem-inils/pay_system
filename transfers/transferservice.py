from datetime import datetime

from sqlalchemy.orm import Session
from database.models import Transfer, Account, User
from database import get_db

from transfers.schemas import CreateTransactionModel


def _validate_account(account_number, db: Session):
    exact_account = db.query(Account).filter_by(account_number=account_number).first()

    return exact_account


def create_transaction_db(
        db: Session,
        data: CreateTransactionModel,
        user: User,
):
    account1 = _validate_account(data.account_from, db)
    account2 = _validate_account(data.account_to, db)

    if account1 and account2:

        if account1.currency == account2.currency:

            if account1.balance >= data.amount:

                try:
                    account1.balance -= data.amount
                    account2.balance += data.amount

                    db.commit()
                    db.refresh(account1)
                    db.refresh(account2)

                except Exception:
                    db.rollback()

                return "Transaction completed"

            else:
                return "Not enough money"
        else:
            return "You can't make transaction. Between two different currencies"
    else:
        return f"Account: {data.account_from} doesn't exist" if account1 else f"Account: {data.account_to} doesn't exist"


def get_card_transaction_db(card_from_id):
    db = next(get_db())

    card_transaction = db.query(Transfer).filter_by(card_from_id=card_from_id).all()

    return card_transaction

# def cancel_transfer_db(card_from, card_to, amount, transfer_id):
#     db = next(get_db())
#
#     check_card_from = _validate_card(card_from, db)
#     check_card_to = _validate_card(card_to, db)
#
#     if check_card_from and check_card_to:
#         if check_card_to.balance >= amount:
#             check_card_from.balance += amount
#             check_card_to.balance -= amount
#
#             transfer = db.query(Transfer).filter_by(transfer_id=transfer_id).first()
#
#             # there was a status here doesn't work
#             db.commit()
#
#             return "перевод успешно отменен"
#         else:
#             return "недостаточно средств на балансе"
#
#     return "Одна из карт не существует"
