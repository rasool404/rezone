from datetime import datetime, timedelta
from typing import Dict, Optional
from .task_base import Task
from .task_base import TaskStatus, Priority
from typing import Any

class SimpleTask(Task):
    """Simple task with optional time limit"""
    
    def __init__(self, task_id: str, title: str, description: str = "", 
                 time_limit_hours: Optional[int] = None, priority: Priority = Priority.MEDIUM):
        super().__init__(task_id, title, description)
        self.time_limit_hours = time_limit_hours
        self.priority = priority
        self.due_date = None
        if time_limit_hours:
            self.due_date = self.created_at + timedelta(hours=time_limit_hours)
    
    def is_expired(self):
        """Check if the task has expired"""
        if not self.time_limit_hours or self.completed:
            return False
        return datetime.now() > self.due_date
    
    def get_status(self):
        """Get the current status of the task"""
        if self.completed:
            return TaskStatus.COMPLETED
        elif self.is_expired():
            return TaskStatus.EXPIRED
        else:
            return TaskStatus.PENDING
    
    def get_time_remaining(self) -> Optional[timedelta]:
        """Get time remaining until due date"""
        if not self.due_date or self.completed:
            return None
        remaining = self.due_date - datetime.now()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def to_dict(self):
        return {
            'type': 'SimpleTask',
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed,
            'time_limit_hours': self.time_limit_hours,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority.value
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'SimpleTask':
        task = cls(data['id'], data['title'], data['description'], 
                  data['time_limit_hours'],
                  Priority(data.get('priority', 'medium')))
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed = data['completed']
        if data['due_date']:
            task.due_date = datetime.fromisoformat(data['due_date'])
        return task