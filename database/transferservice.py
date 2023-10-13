from datetime import datetime

from database.models import Transfer, UserCard
from database import get_db


# поверка карты
def _validate_card(card_number, db):
    exact_card = db.query(UserCard).filter_by(card_number=card_number).first()

    return exact_card


# создать перевод
def create_transaction_db(card_from, card_to, amount):
    db = next(get_db())

    # Проверка на наличие в базе обеих карт
    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    # если обе карты существуют в базе данных
    if check_card_from and check_card_to:
        # проверка баланса токо кто переводит
        if check_card_from.balance >= amount:
            # Минусуем у того кто отправил
            check_card_from.balance -= amount
            # добовляем тому кто получает
            check_card_to.balance += amount
            new_transaction = Transfer(card_from_id=check_card_from.card_id,
                                       card_to_id=check_card_to.card_id,
                                       amount=amount, transaction_date=datetime.now())
            db.add(new_transaction)
            # сохроняем
            db.commit()

            return "перевод успешно выполнен"
        else:
            return "не достаточно средств"

    return "одна из карт не существует"


# Получить все переводы по карте (card_id)
def get_card_transaction_db(card_from_id):
    db = next(get_db())

    card_transaction = db.query(Transfer).filter_by(card_from_id=card_from_id).all()

    return card_transaction


# отмена перевода
def cancel_transfer_db(card_from, card_to, amount, transfer_id):
    db = next(get_db())

    # Проверка на наличие в базе обеих карт
    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    # если обе карты существуют в базе данных
    if check_card_from and check_card_to:
        # проверка баланса токо кто переводит
        if check_card_to.balance >= amount:
            # Минусуем у того кто отправил
            check_card_from.balance += amount
            # добовляем тому кто получает
            check_card_to.balance -= amount

            exact_transaction = db.query(Transfer).filter_by(transfer_id=transfer_id).first()
            exact_transaction.status = False

            # сохроняем
            db.commit()

            return "перевод успешно отменен"
        else:
            return "не достаточно средств"

    return "одна из карт не существует"
