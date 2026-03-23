from aiogram import F, types, Router
from aiogram.filters.command import Command, CommandObject
from db_instanse import db
from config import ADMIN_ID

router = Router()


# Хэндлер для команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}. I'm at your service. What can I do for you?"
    )
    db.insert_user(message.from_user.id, message.from_user.full_name)


# Хэндлер для команды /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "I am a simple bot-helper. Please, enter your message."
    )


# Команда /admin показывает список всех пользователей
@router.message(Command("admin"))
async def cmd_admin(message: types.Message):
    users = db.get_all_users()

    if users:
        txt = "List of users:\n"

        for user in users:
            txt += f"ID: {user[0]} | Имя: {user[1]}\n"

        await message.answer(txt)


# Выводит статистику запросов пользователей
@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    # Благодаря этой проверке команда /stats доступна только админу
    if message.from_user.id != ADMIN_ID:
        await message.answer("Access denied")
        return

    statistics = db.get_statistics()

    if statistics:
        coin_stats = [
            f"User {name} searched {coin} price for {counter} times."
            for name, coin, counter in statistics
        ]

        await message.answer("\n".join(coin_stats))
    else:
        await message.answer("No statistics yet or the query is wrong.")


@router.message(Command("ban"))
async def cmd_ban(message: types.Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Access denied")
        return

    try:
        user_to_block = int(command.args)
    except (ValueError, TypeError):
        await message.answer("Please send a valid ID.")
        return
    else:
        if db.is_user_banned(user_to_block):
            await message.answer("This user has already been banned")
            return

        db.ban_user(user_to_block)
        await message.answer(f"User {user_to_block} has been blocked.")


@router.message(Command("unban"))
async def cmd_unban(message: types.Message, command: CommandObject):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Access denied")
        return

    try:
        user_to_unblock = int(command.args)
    except (ValueError, TypeError):
        await message.answer("Please send a valid ID.")
        return
    else:
        if not db.is_user_banned(user_to_unblock):
            await message.answer("This user is not banned")
            return

        db.unban_user(user_to_unblock)
        await message.answer(f"User {user_to_unblock} has been unblocked.")


# Хэндлер для фото
@router.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("It's a photo, isn't it? Please, send me a text.")


# Хэндлер для остальных сообщений
@router.message(F.text)
async def echo_handler(message: types.Message):
    if message.text == "secret":
        await message.answer(f"Congratulations! You've found a secret word!")
    else:
        await message.answer(
            f"Your message '{message.text}' has been accepted for processing."
        )
