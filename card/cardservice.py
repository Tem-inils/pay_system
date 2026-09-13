from datetime import datetime

from database import get_db
from database.models import Account


def add_card_db(user_id, card_number, balance, card_name, exp_date, cvv):
    db = next(get_db())

    new_card = Account(user_id=user_id, card_number=card_number,
                        balance=balance, card_name=card_name,
                        exp_date=exp_date, cvv=cvv)

    db.add(new_card)
    db.commit()

    return "Карта успешно добавлена"

def delete_exact_card_db(card_id):
    db = next(get_db())

    exact_card = db.query(Account).filter_by(id=card_id).first()

    if exact_card:
        db.delete(exact_card)
        db.commit()

        return "карта успешно удалена"

    return "карта не найдена"

def edit_card_design_db(card_id, design_path):
    db = next(get_db())

    exact_card = db.query(Account).filter_by(id=card_id).first()

    if exact_card:
        exact_card.card_design = design_path
        db.commit()

        return "Дизайн обновлен"

    return "карта не найдена"

def get_exact_user_cards_db(user_id):
    db = next(get_db())

    exact_user_cards = db.query(Account).filter_by(user_id=user_id).all()

    return exact_user_cards

def get_exact_card_db(user_id, card_id):
    db = next(get_db())

    exact_user_card = db.query(Account).filter_by(user_id=user_id, id=card_id).first()

    return exact_user_card

def check_card_info_db(card_number):
    db = next(get_db())

    checker = db.query(Account).filter_by(card_number=card_number).first()

    return checker