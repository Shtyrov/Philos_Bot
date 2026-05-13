import asyncio
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from handlers import router


load_dotenv()


async def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден. Проверь файл .env")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен. Нажми Ctrl+C, чтобы остановить.")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())