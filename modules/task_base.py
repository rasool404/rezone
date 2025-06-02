from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"
    DAILY_PENDING = "daily_pending"
    DAILY_COMPLETED = "daily_completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(ABC):
    def __init__(self, task_id: str, title: str, description: str = ""):
        self.id = task_id
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.completed = False

    @abstractmethod
    def is_expired(self): 
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def from_dict(cls, data):
        pass

    def mark_completed(self):
        self.completed = True

    def mark_incomplete(self):
        self.completed = False