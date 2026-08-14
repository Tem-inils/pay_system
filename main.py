from fastapi import FastAPI

from starlette.templating import Jinja2Templates

from user.user_api import user_router
from card.card_api import card_router
from transfers.transfer_api import transaction_router
from currency.currency_api import currency_router

from dotenv import load_dotenv
load_dotenv()

from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/')

template = Jinja2Templates(directory='templates')

from html_example.html_show import html_router

app.include_router(html_router)

app.include_router(user_router)
app.include_router(card_router)
app.include_router(transaction_router)
app.include_router(currency_router)
