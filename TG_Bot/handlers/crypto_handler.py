import requests
from random import choice

from aiogram import types, Router
from aiogram.filters.command import Command

from db_instanse import db

router = Router()


# Handler for /crypto command
@router.message(Command("crypto"))
async def cmd_crypto(
    message: types.Message, coins: list, currencies: list
) -> None:
    if db.is_user_banned(message.from_user.id):
        await message.answer("Access restricted.")
        return

    # Randomly pick a coins
    coin = choice(coins)
    currency = choice(currencies)

    # # Test: point requests
    # coin = coins[0]
    # currency = currencies[0]

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin['id']}&vs_currencies={currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()

    # If raise_for_status() worked:
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            await message.answer("Too many requests.")
        else:
            await message.answer(f"Server error: {type(http_err).__name__}.")

    # If the error is on the client side(internet lost connection):
    except requests.exceptions.RequestException as req_err:
        await message.answer(
            f"Your request returned an exception: {type(req_err).__name__}."
        )

    else:
        data = response.json()
        raw_price = data.get(coin["id"], {}).get(currency, None)

        # Formatting the price to avoid scientific notation
        if raw_price is not None:
            formatted_price = f"{raw_price:.10f}".rstrip("0").rstrip(".")
        else:
            formatted_price = "No data"

        # Print currency cost
        await message.answer(
            f"The current value of 1 {coin['name']} is {formatted_price} {currency.upper()}."
        )

        # Memorize user's request to database
        db.write_into_log(
            message.from_user.id, f"{coin['name']} / {currency.upper()}"
        )
