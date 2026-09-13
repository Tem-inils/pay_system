from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, Boolean, Numeric, Enum as SqlEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from decimal import Decimal
from enum import Enum
from datetime import datetime
from database import Base

class CardNetwork(str, Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    UNIONPAY = "UNIONPAY"

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    # username: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    city: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    reg_date: Mapped[datetime]= mapped_column()


class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True,)
    account_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True,)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 4), nullable=False, default=Decimal("0.0000"))
    is_acive: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cards: Mapped[list["Card"]] = relationship(back_populates="account")

    created_at: Mapped[datetime]= mapped_column(DateTime, nullable=False)


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,)
    accound_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), nullable=False, index=True,)
    card_number: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True,)
    network: Mapped[CardNetwork] = mapped_column(SqlEnum(CardNetwork), nullable=False,)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True,)
    account: Mapped["Account"] = relationship(back_populates="cards",)

    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class Transfer(Base):
    __tablename__ = 'transfers'
    transfer_id = Column(Integer, primary_key=True, autoincrement=True)
    card_from_id = Column(Integer, ForeignKey('accounts.id'))
    card_to_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)

    status = Column(Boolean, default=True) 

    transaction_date = Column(DateTime)

    card_from_fk = relationship(Account, foreign_keys=[card_from_id], lazy='subquery')
    card_to_fk = relationship(Account, foreign_keys=[card_to_id], lazy='subquery')