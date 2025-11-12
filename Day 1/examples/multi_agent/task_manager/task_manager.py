"""
Core task management logic and business rules.
"""

from datetime import datetime
from typing import List, Optional
from task import Task, TaskStatus, TaskPriority


class TaskManager:
    """Manages tasks with CRUD operations and filtering capabilities."""
    
    def __init__(self, storage):
        """
        Initialize the task manager with a storage backend.
        
        Args:
            storage: Storage implementation (FileStorage, DatabaseStorage, etc.)
        """
        self.storage = storage
        self.tasks = self.storage.load_tasks()
    
    def add_task(self, title: str, description: str = "", 
                 priority: TaskPriority = TaskPriority.MEDIUM, 
                 due_date: Optional[str] = None) -> Task:
        """
        Add a new task to the system.
        
        Args:
            title: Task title (required)
            description: Task description
            priority: Task priority level
            due_date: Due date in YYYY-MM-DD format
            
        Returns:
            Created Task object
        """
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """
        Update task properties.
        
        Args:
            task_id: Unique task identifier
            **kwargs: Task properties to update (title, description, status, priority, due_date)
            
        Returns:
            Updated Task object if found, None otherwise
        """
        task = self.get_task(task_id)
        if not task:
            return None
        
        if 'title' in kwargs:
            task.title = kwargs['title']
        if 'description' in kwargs:
            task.description = kwargs['description']
        if 'status' in kwargs:
            task.status = kwargs['status']
        if 'priority' in kwargs:
            task.priority = kwargs['priority']
        if 'due_date' in kwargs:
            task.due_date = kwargs['due_date']
        
        task.updated_at = datetime.now().isoformat()
        self.storage.save_tasks(self.tasks)
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the system.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            True if task was deleted, False if not found
        """
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.storage.save_tasks(self.tasks)
            return True
        return False
    
    def list_tasks(self, status: Optional[TaskStatus] = None,
                   priority: Optional[TaskPriority] = None,
                   sort_by: str = "created_at") -> List[Task]:
        """
        List tasks with optional filtering and sorting.
        
        Args:
            status: Filter by task status
            priority: Filter by task priority
            sort_by: Sort field (created_at, updated_at, priority, due_date)
            
        Returns:
            List of filtered and sorted Task objects
        """
        filtered_tasks = self.tasks.copy()
        
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]
        
        if priority:
            filtered_tasks = [t for t in filtered_tasks if t.priority == priority]
        
        # Sort tasks
        if sort_by == "priority":
            priority_order = {TaskPriority.HIGH: 3, TaskPriority.MEDIUM: 2, TaskPriority.LOW: 1}
            filtered_tasks.sort(key=lambda t: priority_order.get(t.priority, 0), reverse=True)
        elif sort_by == "due_date":
            filtered_tasks.sort(key=lambda t: t.due_date or "9999-12-31")
        elif sort_by == "updated_at":
            filtered_tasks.sort(key=lambda t: t.updated_at, reverse=True)
        else:  # created_at (default)
            filtered_tasks.sort(key=lambda t: t.created_at, reverse=True)
        
        return filtered_tasks
    
    def get_statistics(self) -> dict:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task statistics
        """
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.status == TaskStatus.COMPLETED])
        pending = len([t for t in self.tasks if t.status == TaskStatus.PENDING])
        in_progress = len([t for t in self.tasks if t.status == TaskStatus.IN_PROGRESS])
        
        high_priority = len([t for t in self.tasks if t.priority == TaskPriority.HIGH])
        overdue = len([t for t in self.tasks if t.is_overdue()])
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress,
            "high_priority": high_priority,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }

