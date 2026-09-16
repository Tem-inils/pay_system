from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.models import Account, User

from account.dependencies import generate_account_number
from account.schemas import CreateAccountModel


def create_account_db(
        db: Session,
        user: User,
        data: CreateAccountModel,
) -> Account:
    new_account = Account(
        user_id=user.id,
        currency=data.currency,
        account_number=generate_account_number(),
    )

    db.add(new_account)

    try:
        db.commit()
        db.refresh(new_account)

        return new_account

    except IntegrityError as error:
        db.rollback()

        print("DATABASE ERROR:")
        print(error.orig)

        raise


def get_all_accounts_db(db: Session, user: User):
    accounts = db.query(Account).filter(Account.user_id == user.id).all()

    return accounts
