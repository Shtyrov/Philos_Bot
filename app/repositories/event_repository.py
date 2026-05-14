from abc import ABC, abstractmethod

from app.domain.event import Event


class EventRepository(ABC):
    @abstractmethod
    async def get_upcoming_events(self) -> list[Event]:
        pass

    @abstractmethod
    async def get_event_by_id(self, event_id: int) -> Event | None:
        pass