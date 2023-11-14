import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import other_handlers, user_handlers
from aiogram.fsm.storage.memory import MemoryStorage
from keyboards.kb import set_main_menu
from dotenv import load_dotenv
load_dotenv()

# Инициализируем бот и диспетчер
bot = Bot(token=os.getenv('tg'), parse_mode='HTML')
dp = Dispatcher(storage=MemoryStorage())

async def main():

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())