from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime

from sqlalchemy.orm import Session
from database import get_db
from database.models import User

from user.dependencies import get_current_user
from transfers.transferservice import create_transaction_db, get_card_transaction_db
from transfers.schemas import CreateTransactionModel, CancelTransactionModel

transaction_router = APIRouter(prefix='/transaction', tags=['Transactions'])


@transaction_router.post('/create')
async def new_transaction(
        data: CreateTransactionModel,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if data.amount > 0:
        return create_transaction_db(db=db, user=current_user, data=data)
    else:
        raise HTTPException(status_code=400, detail="Insufficient funds")

# # Запрос на отмену транзакции
# @transaction_router.post('/cancel')
# async def cancel_transaction(data: CancelTransactionModel):
#     cancel_data = data.model_dump()
#     result = cancel_transfer_db(**cancel_data)
#
#     return {'status': 1, 'message': result}


# Запрос на получение всех транзакций определенной карты
@transaction_router.get('/monitoring')
async def get_card_monitoring(card_id: int):
    result = get_card_transaction_db(card_from_id=card_id)

    return {'status': 1, 'message': result}
