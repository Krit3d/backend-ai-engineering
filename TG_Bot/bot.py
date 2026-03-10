import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from config import BOT_TOKEN
from random import choice

# Список всех монет
COINS_LIST = requests.get("https://api.coingecko.com/api/v3/coins/list").json()
# Список котируемых монет(валют)
COUNTER_CURRENCIES = requests.get(
    "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
).json()

# Включаем логгирование сообщений для отладки
logging.basicConfig(level=logging.INFO)

# Создаём основные объекты: бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Хэндлер для команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}. I'm at your service. What can I do for you?"
    )


# Хэндлер для команды /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "I am a simple bot-helper. Please, enter your message."
    )


# Хэндлер для команды /crypto
@dp.message(Command("crypto"))
async def cmd_crypto(message: types.Message, coins: list, currencies: list):
    coin = choice(coins)
    currency = choice(currencies)

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin['id']}&vs_currencies={currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()

    # Если raise_for_status() сработал
    except requests.exceptions.HTTPError as http_err:
        await message.answer(f"Server error: {type(http_err).__name__}.")

    # Если ошибка на стороне клиента(к примеру, интернет отвалился)
    except requests.exceptions.RequestException as req_err:
        await message.answer(
            f"Your request returned an exception: {type(req_err).__name__}."
        )

    else:
        data = response.json()
        raw_price = data.get(coin['id'], {}).get(currency, None)
    
        # Форматируем цену, чтобы избежать научной записи числа
        if raw_price is not None:
            formatted_price = f"{raw_price:.10f}".rstrip("0").rstrip(".")
        else:
            formatted_price = "No data"

        # Выводим стоимость криптовалюты
        await message.answer(
            f"The current value of 1 {coin['name']} is {formatted_price} {currency.upper()}."
        )


# Хэндлер для фото
@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("It's a photo, isn't it? Please, send me a text.")


# Хэндлер для остальных сообщений
@dp.message()
async def echo_handler(message: types.Message):
    if message.text == "secret":
        await message.answer(f"Congratulations! You've found a secret word!")
    else:
        await message.answer(
            f"Your message '{message.text}' has been accepted for processing."
        )


# Запуск процесса поллинга новых апдейтов
async def main():
    # Удаляем вебхук и пропускаем накопившиеся входящие сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, coins=COINS_LIST, currencies=COUNTER_CURRENCIES)


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())
