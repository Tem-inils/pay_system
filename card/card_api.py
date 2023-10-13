from fastapi import APIRouter

from datetime import datetime

from card import CardAddModel, EditCardModel
from database.cardservice import get_exact_card_db, get_exact_user_cards_db, \
        add_card_db, delete_exact_card_db, edit_card_design_db, \
        check_card_info_db


card_router = APIRouter(prefix='/card', tags=['Работа с картами'])

@card_router.post('/add')
async def add_new_card(data: CardAddModel):
        card_data = data.model_dump()

        checker = check_card_info_db(data.card_number)

        if checker:
            return {'status': 1, 'message': 'карта с таким номером есть в базе'}
        else:
            result = add_card_db(**card_data)
            return {'status': 0, 'message': result}


@card_router.get('/exact-cart-info')
async def get_card_info(card_id: int, user_id: int):
    result = get_exact_card_db(user_id=user_id,
                               card_id=card_id)
    if result:
        return {'status': 1, 'message': result}

    return {'status': 0, 'message': 'карта не найдена'}

@card_router.get('/get-info')
async def get_all_user_cards(user_id: int):
    result = get_exact_user_cards_db(user_id=user_id)

    if result:
        return {'status': 1, 'message': result}

    return {'status': 0, 'message': 'карты не найдены'}

@card_router.delete('/delete-card')
async def delete_exact_card(card_id: int):
    result = delete_exact_card_db(card_id=card_id)

    if result:
        return {'status': 1, 'message': result}



@card_router.put('/edit-card-design')
async def edit_card_design(data: EditCardModel):
    card_data = data.model_dump()

    edit_disgn = edit_card_design_db(**card_data)

    return {'status': 1, 'message': edit_disgn}