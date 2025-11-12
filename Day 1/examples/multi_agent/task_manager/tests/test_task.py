"""
Unit tests for the Task model.
"""

import unittest
from datetime import datetime, timedelta
from task import Task, TaskStatus, TaskPriority


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task(title="Test Task", description="Test Description")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
    
    def test_task_status(self):
        """Test task status changes."""
        task = Task(title="Test", status=TaskStatus.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatus.IN_PROGRESS)
    
    def test_task_priority(self):
        """Test task priority levels."""
        task = Task(title="Test", priority=TaskPriority.HIGH)
        self.assertEqual(task.priority, TaskPriority.HIGH)
    
    def test_task_overdue(self):
        """Test overdue detection."""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        task = Task(title="Overdue", due_date=past_date)
        self.assertTrue(task.is_overdue())
        
        future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        task2 = Task(title="Not Overdue", due_date=future_date)
        self.assertFalse(task2.is_overdue())
    
    def test_task_completed_not_overdue(self):
        """Test that completed tasks are not marked as overdue."""
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        task = Task(title="Completed", due_date=past_date, status=TaskStatus.COMPLETED)
        self.assertFalse(task.is_overdue())
    
    def test_task_serialization(self):
        """Test task to_dict and from_dict."""
        task = Task(
            title="Test",
            description="Description",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH
        )
        
        data = task.to_dict()
        self.assertEqual(data["title"], "Test")
        self.assertEqual(data["status"], "in_progress")
        
        task2 = Task.from_dict(data)
        self.assertEqual(task2.title, task.title)
        self.assertEqual(task2.status, task.status)
        self.assertEqual(task2.priority, task.priority)


if __name__ == "__main__":
    unittest.main()

