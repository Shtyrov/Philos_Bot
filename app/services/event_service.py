from dataclasses import dataclass
from math import ceil

from app.domain.event import Event
from app.repositories.event_repository import EventRepository


@dataclass(frozen=True)
class EventPage:
    events: list[Event]
    page: int
    total_pages: int
    has_previous: bool
    has_next: bool


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def get_events_page(self, page: int = 1, page_size: int = 2) -> EventPage:
        events = await self.repository.get_upcoming_events()

        total_events = len(events)
        total_pages = max(1, ceil(total_events / page_size))

        page = max(1, min(page, total_pages))

        start = (page - 1) * page_size
        end = start + page_size

        return EventPage(
            events=events[start:end],
            page=page,
            total_pages=total_pages,
            has_previous=page > 1,
            has_next=page < total_pages,
        )

    async def get_event_by_id(self, event_id: int) -> Event | None:
        return await self.repository.get_event_by_id(event_id)
