import requests
from random import choice

from aiogram import types, Router
from aiogram.filters.command import Command

from database import write_into_log

router = Router()


# Хэндлер для команды /crypto
@router.message(Command("crypto"))
async def cmd_crypto(message: types.Message, coins: list, currencies: list):
    coin = choice(coins)
    currency = choice(currencies)
    # # Test: point requests
    # coin = coins[0]
    # currency = currencies[0]

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin['id']}&vs_currencies={currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()

    # Если raise_for_status() сработал
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            await message.answer("Too many requests.")
        else:
            await message.answer(f"Server error: {type(http_err).__name__}.")

    # Если ошибка на стороне клиента(к примеру, интернет отвалился)
    except requests.exceptions.RequestException as req_err:
        await message.answer(
            f"Your request returned an exception: {type(req_err).__name__}."
        )

    else:
        data = response.json()
        raw_price = data.get(coin["id"], {}).get(currency, None)

        # Форматируем цену, чтобы избежать научной записи числа
        if raw_price is not None:
            formatted_price = f"{raw_price:.10f}".rstrip("0").rstrip(".")
        else:
            formatted_price = "No data"

        # Выводим стоимость криптовалюты
        await message.answer(
            f"The current value of 1 {coin['name']} is {formatted_price} {currency.upper()}."
        )

        # Заносим запрос пользователя в лог
        write_into_log(
            message.from_user.id, f"{coin['name']} / {currency.upper()}"
        )
