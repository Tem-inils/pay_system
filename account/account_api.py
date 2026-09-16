from fastapi import APIRouter, Depends

from database import get_db
from database.models import User
from sqlalchemy.orm import Session
from account.schemas import CreateAccountModel

from account.accountservice import create_account_db, get_all_accounts_db
from user.dependencies import get_current_user

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.post("/create")
async def create_account(
        data: CreateAccountModel,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return create_account_db(
        db=db,
        user=current_user,
        data=data,
    )


@account_router.get("/all/account")
async def get_all_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_all_accounts_db(db=db, user=current_user)


@account_router.get("/delete")
async def delete_account():
    pass
