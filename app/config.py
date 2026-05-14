import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str


def load_config() -> Config:
    bot_token = os.getenv("BOT_TOKEN")

    if not bot_token:
        raise RuntimeError("BOT_TOKEN не найден. Проверь файл .env")

    return Config(bot_token=bot_token)
