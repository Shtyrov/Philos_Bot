from aiogram import Bot, Dispatcher

from app.bot.handlers import router
from app.config import load_config


async def main() -> None:
    config = load_config()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    dp.include_router(router)

    print("Бот запущен. Нажми Ctrl+C, чтобы остановить.")

    await dp.start_polling(bot)