import os
from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import events_pagination_keyboard
from app.domain.event import Event
from app.repositories.memory_event_repository import MemoryEventRepository
from app.services.event_service import EventPage, EventService


router = Router()

event_repository = MemoryEventRepository()
event_service = EventService(event_repository)

async def delete_trigger_message(message: Message) -> None:
    try:
        await message.delete()
    except Exception:
        pass

def get_bot_username() -> str:
    bot_username = os.getenv("BOT_USERNAME")

    if not bot_username:
        raise RuntimeError("BOT_USERNAME не найден. Проверь файл .env")

    return bot_username.removeprefix("@")


def build_event_details_link(event_id: int) -> str:
    bot_username = get_bot_username()
    return f"https://t.me/{bot_username}?start=event_{event_id}"


def format_events_page(event_page: EventPage) -> str:
    if not event_page.events:
        return "Событий пока нет."

    lines = [
        f"<b>События: страница {event_page.page} из {event_page.total_pages}</b>",
        "",
    ]

    for event in event_page.events:
        starts_at = event.starts_at.strftime("%d.%m.%Y %H:%M")
        details_link = build_event_details_link(event.id)

        lines.extend(
            [
                f"📌 <b>{escape(event.title)}</b>",
                f"Тип: {escape(event.event_type)}",
                f"Когда: {escape(starts_at)}",
                f"Где: {escape(event.location)}",
                f'<a href="{details_link}">Подробнее</a>',
                "",
            ]
        )

    return "\n".join(lines)


def format_event_details(event: Event) -> str:
    starts_at = event.starts_at.strftime("%d.%m.%Y %H:%M")

    source_text = ""
    if event.source_url:
        source_url = escape(event.source_url, quote=True)
        source_text = f'\n\n<a href="{source_url}">Источник</a>'

    return (
        f"📌 <b>{escape(event.title)}</b>\n\n"
        f"<b>Тип:</b> {escape(event.event_type)}\n"
        f"<b>Когда:</b> {escape(starts_at)}\n"
        f"<b>Где:</b> {escape(event.location)}\n\n"
        f"<b>Описание:</b>\n"
        f"{escape(event.description)}"
        f"{source_text}"
    )


async def send_event_details(message: Message, payload: str) -> None:
    if not payload.startswith("event_"):
        await message.answer("Не удалось распознать ссылку на событие.")
        return

    event_id_text = payload.removeprefix("event_")

    if not event_id_text.isdigit():
        await message.answer("Некорректный идентификатор события.")
        return

    event_id = int(event_id_text)
    event = await event_service.get_event_by_id(event_id)

    if event is None:
        await message.answer("Событие не найдено.")
        return

    await message.answer(
        format_event_details(event),
        parse_mode="HTML",
    )


@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject) -> None:
    if command.args:
        await delete_trigger_message(message)
        await send_event_details(message, command.args)
        return

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
        "Раздел событий на сегодня пока находится в разработке.\n\n"
        "Сейчас можно проверить список ближайших событий через /week."
    )


@router.message(Command("week"))
async def week_command(message: Message) -> None:
    event_page = await event_service.get_events_page(page=1)

    await message.answer(
        format_events_page(event_page),
        parse_mode="HTML",
        reply_markup=events_pagination_keyboard(
            page=event_page.page,
            has_previous=event_page.has_previous,
            has_next=event_page.has_next,
        ),
    )


@router.callback_query(F.data.startswith("events:page:"))
async def events_page_callback(callback: CallbackQuery) -> None:
    if callback.data is None:
        await callback.answer()
        return

    if callback.message is None:
        await callback.answer()
        return

    page = int(callback.data.split(":")[-1])
    event_page = await event_service.get_events_page(page=page)

    await callback.message.edit_text(
        format_events_page(event_page),
        parse_mode="HTML",
        reply_markup=events_pagination_keyboard(
            page=event_page.page,
            has_previous=event_page.has_previous,
            has_next=event_page.has_next,
        ),
    )

    await callback.answer()


@router.message(Command("submit"))
async def submit_command(message: Message) -> None:
    await message.answer(
        "Здесь можно будет предложить новое событие.\n\n"
        "В будущем ты сможешь переслать мне анонс, ссылку или текст, "
        "а я попробую собрать из него карточку события."
    )