from fastapi import APIRouter
import requests

from redis_service import redis_db

currency_router = APIRouter(prefix='/currency', tags=['Курсы вылют'])

# проверка редис базы есть ли там информация про курс валюты
def _check_currency_rates_redis():
    checker = redis_db.get("rates")

    if checker:
        return checker

    return False

# запрос на получение всех курсов валют
@currency_router.post('/get-rates')
async def get_currency_rates():
    cb_url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    response = requests.get(cb_url).json()

    # Берем только нужные валюты
    usd_eur_rub_jby = [i for i in response if i['Ccy'] in ['EUR', 'RUB', 'USD', 'JPY']]

    return {'status': 1, 'rates': usd_eur_rub_jby}

