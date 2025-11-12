"""
Storage abstraction layer for task persistence.
"""

import json
import os
from typing import List
from task import Task


class FileStorage:
    """File-based storage implementation using JSON."""
    
    def __init__(self, filepath: str):
        """
        Initialize file storage.
        
        Args:
            filepath: Path to the JSON file for storing tasks
        """
        self.filepath = filepath
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Create the storage file if it doesn't exist."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as f:
                json.dump([], f)
    
    def load_tasks(self) -> List[Task]:
        """
        Load tasks from the storage file.
        
        Returns:
            List of Task objects
        """
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                return [Task.from_dict(task_dict) for task_dict in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_tasks(self, tasks: List[Task]):
        """
        Save tasks to the storage file.
        
        Args:
            tasks: List of Task objects to save
        """
        data = [task.to_dict() for task in tasks]
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear(self):
        """Clear all tasks from storage."""
        with open(self.filepath, 'w') as f:
            json.dump([], f)


class DatabaseStorage:
    """Database storage implementation (placeholder for future implementation)."""
    
    def __init__(self, connection_string: str):
        """
        Initialize database storage.
        
        Args:
            connection_string: Database connection string
        """
        self.connection_string = connection_string
        # TODO: Implement database connection and schema
    
    def load_tasks(self) -> List[Task]:
        """Load tasks from database."""
        # TODO: Implement database query
        raise NotImplementedError("Database storage not yet implemented")
    
    def save_tasks(self, tasks: List[Task]):
        """Save tasks to database."""
        # TODO: Implement database insert/update
        raise NotImplementedError("Database storage not yet implemented")

