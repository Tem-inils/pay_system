from database.models import Account
from account.schemas import CreateAccountModel
from sqlalchemy.orm import Session

def create_account_db(data: CreateAccountModel, db: Session) -> object:
    
    new_account = Account(
        user_id=data.user_id,
        currency=data.currenccy,
        account_number=None,
        
        )