import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher
from handlers import basic_handlers, crypto_handler
from config import BOT_TOKEN

# Request of two lists of coins to work with
COINS_LIST = requests.get("https://api.coingecko.com/api/v3/coins/list").json()
COUNTER_CURRENCIES = requests.get(
    "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
).json()

# Enable logging of messages to debugging
logging.basicConfig(level=logging.INFO)

# Create main objects
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    # Register routers in dispatcher
    dp.include_router(crypto_handler.router)
    dp.include_router(basic_handlers.router)

    # Delete hooks and skip incoming messages
    await bot.delete_webhook(drop_pending_updates=True)
    # Start polling process for new updates
    await dp.start_polling(
        bot,
        coins=COINS_LIST,
        currencies=COUNTER_CURRENCIES,
    )


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
