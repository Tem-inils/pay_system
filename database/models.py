from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

# таблица пользователей
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(Integer, unique=True, nullable=False)
    city = Column(String)
    password = Column(String, nullable=False)
    reg_date = Column(DateTime)


# таблица карт польщователей
class UserCard(Base):
    __tablename__ = 'cards'
    card_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    card_number = Column(Integer, nullable=False)
    balance = Column(Float, default=0)
    exp_date = Column(Integer, nullable=False)
    card_name = Column(String)
    cvv = Column(Integer)
    card_design = Column(String)

    user_fk = relationship(User, lazy='subquery')


# таблица переводов
class Transfer(Base):
    __tablename__ = 'transfers'
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    card_from_id = Column(Integer, ForeignKey('cards.card_id'))
    card_to_id = Column(Integer, ForeignKey('cards.card_id'))
    amount = Column(Float)

    transaction_date = Column(DateTime)
    card_from_fk = relationship(UserCard, foreign_keys=[card_from_id], lazy='subquery')
    card_to_fk = relationship(UserCard, foreign_keys=[card_to_id], lazy='subquery')
