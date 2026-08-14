from pydantic import BaseModel

""" USER API """

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from user.userservice import register_user_db, edit_user_db, delete_user_db, \
                                check_user_existence_db, get_all_user_db, \
                                user_login_db

from database.security import create_access_token, User, get_current_user
from user import UserRegisterModel, EditUserModel, LoginSchema

""" USER SERVICE """

from datetime import datetime

from database.models import User
from database import get_db
from database.security import hash_password, verify_password

###############################################

class UserRegisterModel(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    password: str
    city: str

class EditUserModel(BaseModel):
    user_id: int
    edit_type: str
    new_data: str

class LoginSchema(BaseModel):
    email: str
    password: str

