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
    account_from = _validate_account(data.account_from, db)
    account_to = _validate_account(data.account_to, db)

    if not account_from:
        return f"Account: {data.account_from} doesn't exist"

    if not account_to:
        return f"Account: {data.account_to} doesn't exist"

    if account_from.user_id != user.id:
        return "You can use only an account that belongs to you."

    if account_from.currency != account_to.currency:
        return "You can't make a transaction between different currencies."

    if account_from.balance < data.amount:
        return "Not enough money"

    try:
        account_from.balance -= data.amount
        account_to.balance += data.amount

        transfer = Transfer(
            account_from=account_from.id,
            account_to=account_to.id,
            amount=data.amount,
        )

        db.add(transfer)

        db.commit()

        db.refresh(account_from)
        db.refresh(account_to)
        db.refresh(transfer)

        return "Transaction completed"

    except Exception as e:
        db.rollback()

        print(e)

        return "Something went wrong. Please try again later."


def get_transaction_db(db: Session, user: User):
    pass


def cancel_transaction_db(db: Session, user: User):
    pass



