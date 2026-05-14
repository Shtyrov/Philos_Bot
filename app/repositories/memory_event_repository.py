from datetime import datetime

from app.domain.event import Event
from app.repositories.event_repository import EventRepository


class MemoryEventRepository(EventRepository):
    def __init__(self) -> None:
        self._events = [
            Event(
                id=1,
                title="Семинар по философии сознания",
                starts_at=datetime(2026, 5, 20, 18, 0),
                location="Онлайн",
                event_type="Семинар",
                description="Тестовое событие для проверки отображения списка мероприятий.",
                source_url=None,
            ),
            Event(
                id=2,
                title="Доклад о каузальной теории действия",
                starts_at=datetime(2026, 5, 22, 17, 30),
                location="Москва, МГУ",
                event_type="Доклад",
                description="Тестовый доклад по философии действия.",
                source_url=None,
            ),
            Event(
                id=3,
                title="CFP: конференция по философии ИИ",
                starts_at=datetime(2026, 5, 30, 23, 59),
                location="Дедлайн подачи тезисов",
                event_type="CFP",
                description="Тестовый дедлайн для будущего раздела CFP.",
                source_url=None,
            ),
        ]

    async def get_upcoming_events(self) -> list[Event]:
        return sorted(self._events, key=lambda event: event.starts_at)

    async def get_event_by_id(self, event_id: int) -> Event | None:
        for event in self._events:
            if event.id == event_id:
                return event

        return None
