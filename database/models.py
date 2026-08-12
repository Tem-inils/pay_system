from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    city: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    reg_date: Mapped[datetime]= mapped_column()


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


class Transfer(Base):
    __tablename__ = 'transfers'
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    card_from_id = Column(Integer, ForeignKey('cards.card_id'))
    card_to_id = Column(Integer, ForeignKey('cards.card_id'))
    amount = Column(Float)

    status = Column(Boolean, default=True) 

    transaction_date = Column(DateTime)

    card_from_fk = relationship(UserCard, foreign_keys=[card_from_id], lazy='subquery')
    card_to_fk = relationship(UserCard, foreign_keys=[card_to_id], lazy='subquery')