from fastapi import APIRouter, Depends
import requests

currency_router = APIRouter(prefix='/currency', tags=['Курсы вылют'])

# запрос на получение всех курсов валют
@currency_router.post('/get-rates')
async def get_currency_rates():
    cb_url = 'https://cbu.uz/ru/arkhiv-kursov-valyut/json/'
    response = requests.get(cb_url).json()

    # Берем только нужные валюты
    usd_eur_rub_jby = [i for i in response if i['Ccy'] in ['EUR', 'RUB', 'USD', 'JPY']]

    return {'status': 1, 'rates': usd_eur_rub_jby}

