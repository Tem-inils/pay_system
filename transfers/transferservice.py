from datetime import datetime

from database.models import Transfer, UserCard
from database import get_db


def _validate_card(card_number, db):
    exact_card = db.query(UserCard).filter_by(card_number=card_number).first()

    return exact_card


def create_transaction_db(card_from, card_to, amount):
    db = next(get_db())

    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    if check_card_from and check_card_to:
        if check_card_from.balance >= amount:
            check_card_from.balance -= amount
            check_card_to.balance += amount

            new_transaction = Transfer(card_from_id=check_card_from.card_id,
                                       card_to_id=check_card_to.card_id,
                                       amount=amount,
                                       transaction_date=datetime.now())
            db.add(new_transaction)
            db.commit()

            # выдаем ответ
            return "перевод успешно выполнен"

        else:
        
            return "недостаточно средств на балансе"

    return "Одна из карт не существует"


def get_card_transaction_db(card_from_id):
    db = next(get_db())

    card_transaction = db.query(Transfer).filter_by(card_from_id=card_from_id).all()

    return card_transaction


def cancel_transfer_db(card_from, card_to, amount, transfer_id):
    db = next(get_db())

    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    if check_card_from and check_card_to:
        if check_card_to.balance >= amount:
            check_card_from.balance += amount
            check_card_to.balance -= amount

            transfer = db.query(Transfer).filter_by(transfer_id=transfer_id).first()
            
            # there was a status here doesn't work 
            db.commit()

            return "перевод успешно отменен"
        else:
            return "недостаточно средств на балансе"

    return "Одна из карт не существует"