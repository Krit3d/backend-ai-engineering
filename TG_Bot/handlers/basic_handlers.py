from aiogram import F, types, Router
from aiogram.filters.command import Command

router = Router()


# Хэндлер для команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Hello, {message.from_user.full_name}. I'm at your service. What can I do for you?"
    )


# Хэндлер для команды /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "I am a simple bot-helper. Please, enter your message."
    )


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
