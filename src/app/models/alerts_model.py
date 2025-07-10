from datetime import datetime

from .event_model import Event


class Alert:
    def __init__(self, triggered_at: datetime, events: list[Event]):
        self.triggered_at = triggered_at
        self.events = events

    def to_dict(self):
        return {
            "triggered_at": self.triggered_at.isoformat(),
            "events": [e.raw for e in self.events]
        }
