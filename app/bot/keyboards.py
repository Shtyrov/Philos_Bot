from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def events_pagination_keyboard(
    page: int,
    has_previous: bool,
    has_next: bool,
) -> InlineKeyboardMarkup | None:
    buttons = []

    if has_previous:
        buttons.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"events:page:{page - 1}",
            )
        )

    if has_next:
        buttons.append(
            InlineKeyboardButton(
                text="Вперед ➡️",
                callback_data=f"events:page:{page + 1}",
            )
        )

    if not buttons:
        return None

    return InlineKeyboardMarkup(inline_keyboard=[buttons])
