from fastapi import APIRouter

from datetime import datetime

from database.transferservice import create_transaction_db, cancel_transfer_db, \
                                     get_card_transaction_db
from transfers import CreateTransactionModel, CancelTransactionModel

transaction_router = APIRouter(prefix='/transaction', tags=['Работа с платежами'])


# Запрос на создание транзакции
@transaction_router.post('/create')
async def add_new_transaction(data: CreateTransactionModel):
    transaction_data = data.model_dump()
    result = create_transaction_db(**transaction_data)

    return {'status': 1, 'message': result}


# Запрос на отмену транзакции
@transaction_router.post('/cancel')
async def cancel_transaction(data: CancelTransactionModel):
    cancel_data = data.model_dump()
    result = cancel_transfer_db(**cancel_data)

    return {'status': 1, 'message': result}


# Запрос на получение всех транзакций определенной карты
@transaction_router.get('/monitoring')
async def get_card_monitoring(card_id: int):
    result = get_card_transaction_db(card_from_id=card_id)

    return {'status': 1, 'message': result}
