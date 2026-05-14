import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    bot_username: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")
    bot_username = os.getenv("BOT_USERNAME")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден. Проверь файл .env")

    if not bot_username:
        raise RuntimeError("BOT_USERNAME не найден. Проверь файл .env")

    return Config(
        bot_token=bot_token,
        bot_username=bot_username.removeprefix("@"),
    )
