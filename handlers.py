from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer(
        "Привет! Я бот-календарь академических философских мероприятий.\n\n"
        "Я помогу следить за докладами, конференциями, семинарами и дедлайнами."
    )


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Доступные команды:\n\n"
        "/start — запустить бота\n"
        "/help — показать список команд\n"
        "/today — события сегодня\n"
        "/week — события на неделю\n"
        "/submit — предложить новое событие"
    )


@router.message(Command("today"))
async def today_command(message: Message) -> None:
    await message.answer(
        "На сегодня событий пока нет.\n\n"
        "Позже здесь будут отображаться ближайшие философские мероприятия на текущий день."
    )


@router.message(Command("week"))
async def week_command(message: Message) -> None:
    await message.answer(
        "На этой неделе событий пока нет.\n\n"
        "Позже здесь будет список ближайших докладов, конференций, семинаров и CFP."
    )


@router.message(Command("submit"))
async def submit_command(message: Message) -> None:
    await message.answer(
        "Здесь можно будет предложить новое событие.\n\n"
        "В будущем ты сможешь переслать мне анонс, ссылку или текст, "
        "а я попробую собрать из него карточку события."
    )