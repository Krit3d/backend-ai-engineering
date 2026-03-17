import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher
from handlers import basic_handlers, crypto_handler
from config import BOT_TOKEN
from database import db_start, create_requests_log

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


# Запуск процесса поллинга новых апдейтов
async def main():
    # Создание таблицы с пользователями
    db_start()
    # Побочная таблица, хранящая запросы пользователей
    create_requests_log()

    # Регистрируем роутеры в диспетчере
    dp.include_router(crypto_handler.router)
    dp.include_router(basic_handlers.router)

    # Удаляем вебхук и пропускаем накопившиеся входящие сообщения
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot,
        coins=COINS_LIST,
        currencies=COUNTER_CURRENCIES,
    )


# Точка входа в программу
if __name__ == "__main__":
    asyncio.run(main())
