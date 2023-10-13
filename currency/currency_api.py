from fastapi import APIRouter, Depends
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
async def get_currency_rates(redis_checker=Depends(_check_currency_rates_redis)):
    # Если в редисе есть данные то показываем оттуда
    if redis_checker:
        print('Достал из редиса')
        return {'status': 1, 'rates': redis_checker.decode()}


    # а если в редисе нечего нет, переходи по ссылке и записываем
    cb_url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    response = requests.get(cb_url).json()

    # Берем только нужные валюты
    usd_eur_rub_jby = [i for i in response if i['Ccy'] in ['EUR', 'RUB', 'USD', 'JPY']]

    # сохроним в редис базу
    redis_db.set("rates", usd_eur_rub_jby)
    print('not redis')

    return {'status': 1, 'rates': usd_eur_rub_jby}

