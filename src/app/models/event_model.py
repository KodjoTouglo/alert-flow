from datetime import datetime

class Event:
    def __init__(self, raw: dict, timestamp_key="timestamp", level_key="level", message_key="message"):
        self.raw = raw
        self.timestamp = datetime.fromisoformat(raw[timestamp_key].replace("Z", "+00:00"))
        self.level = raw.get(level_key, "").upper()
        self.message = raw.get(message_key, "")

    def __repr__(self):
        return f"[{self.timestamp}] {self.level} - {self.message}"
