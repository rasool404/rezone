from datetime import datetime
from typing import Dict, List, Optional, Callable
import json
import os
from .task_base import Task
from .task_base import TaskStatus, Priority
from .simple_task import SimpleTask
from .daily_task import DailyTask
from .exceptions import TaskManagerError



class TaskManager:
    """Core task manager class"""
    def __init__(self, data_file: Optional[str] = None, auto_save: bool = True):
        self.data_file = data_file
        self.auto_save = auto_save
        self.tasks: Dict[str, Task] = {}
        self._task_counter = 0
        self._event_handlers: Dict[str, List[Callable]] = {
            'task_added': [],
            'task_completed': [],
            'task_removed': [],
            'task_expired': []
        }
        
        if self.data_file:
            self.load_tasks()
        self.refresh_daily_tasks()
    
    def generate_task_id(self) -> str:
        """Generate a unique task ID"""
        self._task_counter += 1
        return f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._task_counter}"
    
    def add_event_handler(self, event: str, handler: Callable):
        """Add an event handler for task events"""
        if event in self._event_handlers:
            self._event_handlers[event].append(handler)
    
    def _trigger_event(self, event: str, task: Task):
        """Trigger event handlers"""
        for handler in self._event_handlers.get(event, []):
            try:
                handler(task)
            except Exception:
                pass 
    
    def add_simple_task(self, title: str, description: str = "", 
                       time_limit_hours: Optional[int] = None, 
                       task_id: Optional[str] = None,
                       priority: Priority = Priority.MEDIUM) -> str:
        """Add a new simple task and return its ID"""
        if not task_id:
            task_id = self.generate_task_id()
        
        if task_id in self.tasks:
            raise TaskManagerError(f"Task ID '{task_id}' already exists")
        
        task = SimpleTask(task_id, title, description, time_limit_hours, priority)
        self.tasks[task_id] = task
        
        if self.auto_save and self.data_file:
            self.save_tasks()
        
        self._trigger_event('task_added', task)
        return task_id

    
    def add_daily_task(self, title: str, description: str = "", 
                      reset_hour: int = 0, task_id: Optional[str] = None) -> str:
        """Add a new daily task and return its ID"""
        if not task_id:
            task_id = self.generate_task_id()
        
        if task_id in self.tasks:
            raise TaskManagerError(f"Task ID '{task_id}' already exists")
        
        task = DailyTask(task_id, title, description, reset_hour)
        self.tasks[task_id] = task
        
        if self.auto_save and self.data_file:
            self.save_tasks()
        
        self._trigger_event('task_added', task)
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Task]:
        """Get all tasks"""
        return self.tasks.copy()
    
    def get_tasks_by_status(self, status: TaskStatus) -> Dict[str, Task]:
        """Get tasks filtered by status"""
        return {tid: task for tid, task in self.tasks.items() 
                if task.get_status() == status}
    
    def get_tasks_by_type(self, task_type: type) -> Dict[str, Task]:
        """Get tasks filtered by type"""
        return {tid: task for tid, task in self.tasks.items() 
                if isinstance(task, task_type)}
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        task.mark_completed()
        
        if self.auto_save and self.data_file:
            self.save_tasks()
        
        self._trigger_event('task_completed', task)
        return True
    
    def remove_task(self, task_id: str) -> bool:
        """Remove a task"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks.pop(task_id)
        
        if self.auto_save and self.data_file:
            self.save_tasks()
        
        self._trigger_event('task_removed', task)
        return True
    
    def refresh_daily_tasks(self):
        """Check and reset daily tasks if needed"""
        for task in self.tasks.values():
            if isinstance(task, DailyTask):
                task.reset_if_needed()
        
        if self.auto_save and self.data_file:
            self.save_tasks()
    
    def get_expired_tasks(self) -> Dict[str, Task]:
        """Get all expired tasks"""
        expired = {}
        for task_id, task in self.tasks.items():
            if task.is_expired():
                expired[task_id] = task
                self._trigger_event('task_expired', task)
        return expired
    
    def save_tasks(self, file_path: Optional[str] = None):
        """Save tasks to JSON file"""
        if not file_path:
            file_path = self.data_file
        
        if not file_path:
            raise TaskManagerError("No file path specified for saving")
        
        try:
            data = [task.to_dict() for task in self.tasks.values()]
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise TaskManagerError(f"Failed to save tasks: {e}")
    
    def load_tasks(self, file_path: Optional[str] = None):
        """Load tasks from JSON file"""
        if not file_path:
            file_path = self.data_file
        
        if not file_path or not os.path.exists(file_path):
            return
        
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.tasks = {}
            for task_data in data:
                if task_data['type'] == 'SimpleTask':
                    task = SimpleTask.from_dict(task_data)
                elif task_data['type'] == 'DailyTask':
                    task = DailyTask.from_dict(task_data)
                else:
                    continue
                self.tasks[task.id] = task
        except Exception as e:
            raise TaskManagerError(f"Failed to load tasks: {e}")

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about tasks"""
        stats = {
            'total': len(self.tasks),
            'completed': 0,
            'pending': 0,
            'expired': 0,
            'daily_tasks': 0,
            'simple_tasks': 0,
            'high_priority_completed': 0,
            'medium_priority_completed': 0,
            'low_priority_completed': 0
        }
        
        for task in self.tasks.values():
            status = task.get_status()
            if status == TaskStatus.COMPLETED or status == TaskStatus.DAILY_COMPLETED:
                stats['completed'] += 1
            elif status == TaskStatus.EXPIRED:
                stats['expired'] += 1
            else:
                stats['pending'] += 1
            
            if isinstance(task, DailyTask):
                stats['daily_tasks'] += 1
            else:
                stats['simple_tasks'] += 1
        
        return stats
    