from app.models.event_model import Event
import json

def load_events(file_path="events.log") -> list[Event]:
    events = []
    with open(file_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line)
                events.append(Event(data))
            except:
                continue
    return events
