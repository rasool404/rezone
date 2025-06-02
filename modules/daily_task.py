from datetime import datetime
from typing import Dict, Any
from .task_base import Task, TaskStatus

class DailyTask(Task):
    """Daily recurring task that resets every day"""
    
    def __init__(self, task_id: str, title: str, description: str = "", 
                 reset_hour: int = 0):
        super().__init__(task_id, title, description)
        self.last_completed_date = None
        self.reset_hour = reset_hour 
    
    def is_expired(self) -> bool:
        """Daily tasks don't expire, they reset"""
        return False
    
    def get_status(self) -> TaskStatus:
        """Get the current status of the task"""
        self.reset_if_needed()
        if self.completed:
            return TaskStatus.DAILY_COMPLETED
        else:
            return TaskStatus.DAILY_PENDING
    
    def should_reset(self) -> bool:
        """Check if the task should be reset for today"""
        if not self.last_completed_date:
            return False
        
        now = datetime.now()
        today = now.date()
        
        # If completed today, no need to reset
        if self.last_completed_date.date() == today:
            return False
        
        # If completed before today, should reset
        return True
    
    def reset_if_needed(self):
        """Reset the task if it's a new day"""
        if self.should_reset():
            self.completed = False
    
    def mark_completed(self):
        """Mark daily task as completed and record the date"""
        super().mark_completed()
        self.last_completed_date = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'type': 'DailyTask',
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed,
            'last_completed_date': self.last_completed_date.isoformat() if self.last_completed_date else None,
            'reset_hour': self.reset_hour,
        }
    
    def from_dict(cls, data: Dict[str, Any]) -> 'DailyTask':
        task = cls(data['id'], data['title'], data['description'], 
                  data.get('reset_hour', 0))
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed = data['completed']
        if data['last_completed_date']:
            task.last_completed_date = datetime.fromisoformat(data['last_completed_date'])
        return task