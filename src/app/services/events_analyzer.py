from collections import deque
from datetime import timedelta

from app.configs.config import Config
from app.models.alerts_model import Alert
from app.models.event_model import Event


class EventAnalyzer:
    def __init__(self):
        config = Config()
        window_seconds = config.get("event_analyzer.window_seconds", 30)
        critical_levels = config.get("event_analyzer.critical_levels", ["CRITICAL"])

        self.window = timedelta(seconds=window_seconds)
        self.buffer = deque()
        self.critical_levels = set(critical_levels)

    def analyze(self, event: Event) -> Alert | None:
        if event.level not in self.critical_levels:
            return None
        self.buffer.append(event)
        while self.buffer and (event.timestamp - self.buffer[0].timestamp) > self.window:
            self.buffer.popleft()
        if len(self.buffer) >= 3:
            group = list(self.buffer)
            self.buffer.clear()
            return Alert(triggered_at=event.timestamp, events=group)
        return None
