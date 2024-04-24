import requests
import aiohttp
from fastapi import HTTPException


def sync_converter(from_currency: str, to_currency: str, price: float):
    to_currency = f'{from_currency}-{to_currency}'
    url = f'https://economia.awesomeapi.com.br/last/{to_currency}'

    try:
        response = requests.get(url=url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)

    data = response.json()

    if "status" in data:
        raise HTTPException(
            status_code=data["status"], detail='Coin not exists')

    from_currency, to_currency = to_currency.split('-')
    coin = from_currency + to_currency
    result = float(data[coin]["bid"])

    return price * result


async def async_converter(from_currency: str, to_currency: str, price: float):
    to_currency = f'{from_currency}-{to_currency}'
    url = f'https://economia.awesomeapi.com.br/last/{to_currency}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json()
    except Exception as error:
        raise HTTPException(status_code=400, detail=error)

    if "status" in data:
        raise HTTPException(
            status_code=data["status"], detail='Coin not exists')

    from_currency, to_currency = to_currency.split('-')
    coin = from_currency + to_currency
    result = float(data[coin]["bid"])

    return {to_currency: price * result}
