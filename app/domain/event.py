from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    id: int
    title: str
    starts_at: datetime
    location: str
    event_type: str
    description: str
    source_url: str | None = None
