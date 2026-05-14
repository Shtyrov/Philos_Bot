from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import events_pagination_keyboard
from app.repositories.memory_event_repository import MemoryEventRepository
from app.services.event_service import EventPage, EventService


router = Router()

event_repository = MemoryEventRepository()
event_service = EventService(event_repository)


def format_events_page(event_page: EventPage) -> str:
    if not event_page.events:
        return "Событий пока нет."

    lines = [
        f"События: страница {event_page.page} из {event_page.total_pages}",
        "",
    ]

    for event in event_page.events:
        starts_at = event.starts_at.strftime("%d.%m.%Y %H:%M")

        lines.extend(
            [
                f"📌 {event.title}",
                f"Тип: {event.event_type}",
                f"Когда: {starts_at}",
                f"Где: {event.location}",
                "",
            ]
        )

    return "\n".join(lines)


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
        "Раздел событий на сегодня пока находится в разработке.\n\n"
        "Сейчас можно проверить список ближайших событий через /week."
    )


@router.message(Command("week"))
async def week_command(message: Message) -> None:
    event_page = await event_service.get_events_page(page=1)

    await message.answer(
        format_events_page(event_page),
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

    page = int(callback.data.split(":")[-1])
    event_page = await event_service.get_events_page(page=page)

    await callback.message.edit_text(
        format_events_page(event_page),
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
