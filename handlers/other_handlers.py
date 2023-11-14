from aiogram import F, Router

router = Router()

from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEX

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    await message.answer(text=LEX['other_answer'])