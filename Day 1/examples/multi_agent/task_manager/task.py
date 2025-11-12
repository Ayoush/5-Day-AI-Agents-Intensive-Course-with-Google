"""
Task data model and related enums.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class TaskStatus(Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    """Represents a single task in the system."""
    
    def __init__(self, title: str, description: str = "",
                 status: TaskStatus = TaskStatus.PENDING,
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 due_date: Optional[str] = None,
                 task_id: Optional[str] = None,
                 created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        """
        Initialize a new task.
        
        Args:
            title: Task title
            description: Task description
            status: Current task status
            priority: Task priority level
            due_date: Due date in YYYY-MM-DD format
            task_id: Unique identifier (auto-generated if not provided)
            created_at: Creation timestamp (auto-generated if not provided)
            updated_at: Last update timestamp (auto-generated if not provided)
        """
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status if isinstance(status, TaskStatus) else TaskStatus(status)
        self.priority = priority if isinstance(priority, TaskPriority) else TaskPriority(priority)
        self.due_date = due_date
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def is_overdue(self) -> bool:
        """
        Check if the task is overdue.
        
        Returns:
            True if task is overdue, False otherwise
        """
        if not self.due_date or self.status == TaskStatus.COMPLETED:
            return False
        
        try:
            due = datetime.fromisoformat(self.due_date)
            return datetime.now() > due
        except (ValueError, TypeError):
            return False
    
    def to_dict(self) -> dict:
        """
        Convert task to dictionary for serialization.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority.value,
            "due_date": self.due_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task instance from a dictionary.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task instance
        """
        return cls(
            task_id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            status=TaskStatus(data.get("status", "pending")),
            priority=TaskPriority(data.get("priority", "medium")),
            due_date=data.get("due_date"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        status_icon = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.CANCELLED: "❌"
        }
        priority_icon = {
            TaskPriority.LOW: "⬇️",
            TaskPriority.MEDIUM: "➡️",
            TaskPriority.HIGH: "⬆️"
        }
        
        icon = status_icon.get(self.status, "📝")
        priority = priority_icon.get(self.priority, "")
        overdue = "⚠️ OVERDUE" if self.is_overdue() else ""
        
        return f"{icon} [{self.id[:8]}] {self.title} {priority} {overdue}".strip()
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Task(id={self.id}, title={self.title!r}, status={self.status.value})"

