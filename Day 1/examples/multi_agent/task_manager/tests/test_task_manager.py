"""
Unit tests for the TaskManager class.
"""

import unittest
import os
import tempfile
from task_manager import TaskManager
from storage import FileStorage
from task import TaskStatus, TaskPriority


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = FileStorage(self.temp_file.name)
        self.manager = TaskManager(self.storage)
    
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task("Test Task", "Description", TaskPriority.HIGH)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(len(self.manager.tasks), 1)
    
    def test_get_task(self):
        """Test retrieving a task."""
        task = self.manager.add_task("Test Task")
        retrieved = self.manager.get_task(task.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, task.id)
    
    def test_update_task(self):
        """Test updating a task."""
        task = self.manager.add_task("Original Title")
        updated = self.manager.update_task(task.id, title="Updated Title", status=TaskStatus.IN_PROGRESS)
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.status, TaskStatus.IN_PROGRESS)
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = self.manager.add_task("To Delete")
        self.assertTrue(self.manager.delete_task(task.id))
        self.assertIsNone(self.manager.get_task(task.id))
        self.assertFalse(self.manager.delete_task("nonexistent"))
    
    def test_list_tasks_filtered(self):
        """Test listing tasks with filters."""
        self.manager.add_task("Task 1", priority=TaskPriority.HIGH)
        self.manager.add_task("Task 2", priority=TaskPriority.LOW)
        self.manager.add_task("Task 3", priority=TaskPriority.HIGH, status=TaskStatus.COMPLETED)
        
        high_priority = self.manager.list_tasks(priority=TaskPriority.HIGH)
        self.assertEqual(len(high_priority), 2)
        
        completed = self.manager.list_tasks(status=TaskStatus.COMPLETED)
        self.assertEqual(len(completed), 1)
    
    def test_get_statistics(self):
        """Test getting task statistics."""
        self.manager.add_task("Task 1", status=TaskStatus.PENDING)
        self.manager.add_task("Task 2", status=TaskStatus.IN_PROGRESS)
        self.manager.add_task("Task 3", status=TaskStatus.COMPLETED, priority=TaskPriority.HIGH)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 1)
        self.assertEqual(stats["in_progress"], 1)
        self.assertEqual(stats["high_priority"], 1)


if __name__ == "__main__":
    unittest.main()

