from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Event(BaseModel):
    timestamp: datetime = Field(...)
    event_type: str = Field(...)
    priority: Priority = Field(...)
    message: str = Field(...)

