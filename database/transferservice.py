from datetime import datetime

from database.models import Transfer, UserCard
from database import get_db


# проверка карты
def _validate_card(card_number, db):
    exact_card = db.query(UserCard).filter_by(card_number=card_number).first()

    return exact_card


# Создать перевод
def create_transaction_db(card_from, card_to, amount):
    db = next(get_db())

    # Проверка на наличие в базе обеих карт
    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    # Если обе карты существуют в базе данных
    if check_card_from and check_card_to:
        # проверка баланса того кто переводит деньги
        if check_card_from.balance >= amount:
            # Минусуем у того кто отправил
            check_card_from.balance -= amount
            # добавляем тому кто получает
            check_card_to.balance += amount

            # сохраняем в базе
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


# Получить все переводы по карте (card_id)
def get_card_transaction_db(card_from_id):
    db = next(get_db())

    card_transaction = db.query(Transfer).filter_by(card_from_id=card_from_id).all()

    return card_transaction


# Отменить перевод
def cancel_transfer_db(card_from, card_to, amount, transfer_id):
    db = next(get_db())

    # Проверка на наличие в базе обеих карт
    check_card_from = _validate_card(card_from, db)
    check_card_to = _validate_card(card_to, db)

    # Если обе карты существуют в базе данных
    if check_card_from and check_card_to:
        # проверка баланса того кто возвращает деньги
        if check_card_to.balance >= amount:
            # добавляем у того кто отправил до этого
            check_card_from.balance += amount
            # отнимаем тому кто получил до этого
            check_card_to.balance -= amount

            # сохраняем в базе
            exact_transaction = db.query(Transfer).filter_by(transfer_id=transfer_id).first()
            exact_transaction.status = False

            db.commit()

            # выдаем ответ
            return "перевод успешно отменен"
        else:
            return "недостаточно средств на балансе"

    return "Одна из карт не существует"