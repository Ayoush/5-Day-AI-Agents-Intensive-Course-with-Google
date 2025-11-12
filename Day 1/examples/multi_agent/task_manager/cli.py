"""
Command-line interface for the task management system.
"""

import sys
from typing import List
from task_manager import TaskManager
from task import TaskStatus, TaskPriority


class TaskCLI:
    """Command-line interface handler."""
    
    def __init__(self, manager: TaskManager):
        """
        Initialize the CLI with a task manager.
        
        Args:
            manager: TaskManager instance
        """
        self.manager = manager
    
    def run(self):
        """Run the interactive CLI loop."""
        print("=" * 60)
        print("Welcome to Task Manager CLI!")
        print("=" * 60)
        print("\nAvailable commands:")
        print("  add <title> [description] [priority] [due_date]")
        print("  list [status] [priority] [sort_by]")
        print("  update <id> [field=value ...]")
        print("  delete <id>")
        print("  show <id>")
        print("  stats")
        print("  help")
        print("  exit")
        print()
        
        while True:
            try:
                command = input("task> ").strip()
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                
                parts = command.split()
                self.handle_command(parts)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def handle_command(self, args: List[str]):
        """
        Handle a command with arguments.
        
        Args:
            args: List of command arguments
        """
        if not args:
            return
        
        command = args[0].lower()
        
        if command == "add":
            self._handle_add(args[1:])
        elif command == "list":
            self._handle_list(args[1:])
        elif command == "update":
            self._handle_update(args[1:])
        elif command == "delete":
            self._handle_delete(args[1:])
        elif command == "show":
            self._handle_show(args[1:])
        elif command == "stats":
            self._handle_stats()
        elif command == "help":
            self._handle_help()
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def _handle_add(self, args: List[str]):
        """Handle add command."""
        if not args:
            print("Usage: add <title> [description] [priority] [due_date]")
            return
        
        title = args[0]
        description = args[1] if len(args) > 1 else ""
        priority = TaskPriority(args[2]) if len(args) > 2 else TaskPriority.MEDIUM
        due_date = args[3] if len(args) > 3 else None
        
        try:
            task = self.manager.add_task(title, description, priority, due_date)
            print(f"✅ Task added: {task}")
        except Exception as e:
            print(f"Error adding task: {e}")
    
    def _handle_list(self, args: List[str]):
        """Handle list command."""
        status = None
        priority = None
        sort_by = "created_at"
        
        for arg in args:
            if arg.startswith("status="):
                status = TaskStatus(arg.split("=")[1])
            elif arg.startswith("priority="):
                priority = TaskPriority(arg.split("=")[1])
            elif arg.startswith("sort="):
                sort_by = arg.split("=")[1]
        
        tasks = self.manager.list_tasks(status=status, priority=priority, sort_by=sort_by)
        
        if not tasks:
            print("No tasks found.")
            return
        
        print(f"\n📋 Tasks ({len(tasks)}):")
        print("-" * 60)
        for task in tasks:
            print(f"  {task}")
            if task.description:
                print(f"    └─ {task.description[:50]}...")
        print()
    
    def _handle_update(self, args: List[str]):
        """Handle update command."""
        if not args:
            print("Usage: update <id> [field=value ...]")
            return
        
        task_id = args[0]
        updates = {}
        
        for arg in args[1:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                if key == "status":
                    updates["status"] = TaskStatus(value)
                elif key == "priority":
                    updates["priority"] = TaskPriority(value)
                else:
                    updates[key] = value
        
        task = self.manager.update_task(task_id, **updates)
        if task:
            print(f"✅ Task updated: {task}")
        else:
            print(f"❌ Task not found: {task_id}")
    
    def _handle_delete(self, args: List[str]):
        """Handle delete command."""
        if not args:
            print("Usage: delete <id>")
            return
        
        task_id = args[0]
        if self.manager.delete_task(task_id):
            print(f"✅ Task deleted: {task_id}")
        else:
            print(f"❌ Task not found: {task_id}")
    
    def _handle_show(self, args: List[str]):
        """Handle show command."""
        if not args:
            print("Usage: show <id>")
            return
        
        task = self.manager.get_task(args[0])
        if task:
            print(f"\n📝 Task Details:")
            print(f"  ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  Description: {task.description or '(none)'}")
            print(f"  Status: {task.status.value}")
            print(f"  Priority: {task.priority.value}")
            print(f"  Due Date: {task.due_date or '(none)'}")
            print(f"  Created: {task.created_at}")
            print(f"  Updated: {task.updated_at}")
            if task.is_overdue():
                print(f"  ⚠️  OVERDUE")
        else:
            print(f"❌ Task not found: {args[0]}")
    
    def _handle_stats(self):
        """Handle stats command."""
        stats = self.manager.get_statistics()
        print("\n📊 Task Statistics:")
        print(f"  Total Tasks: {stats['total']}")
        print(f"  ✅ Completed: {stats['completed']}")
        print(f"  ⏳ Pending: {stats['pending']}")
        print(f"  🔄 In Progress: {stats['in_progress']}")
        print(f"  ⬆️  High Priority: {stats['high_priority']}")
        print(f"  ⚠️  Overdue: {stats['overdue']}")
        print(f"  📈 Completion Rate: {stats['completion_rate']:.1f}%")
        print()
    
    def _handle_help(self):
        """Handle help command."""
        print("\nAvailable Commands:")
        print("  add <title> [description] [priority] [due_date]")
        print("     - Add a new task")
        print("     - Priority: low, medium, high")
        print("     - Due date format: YYYY-MM-DD")
        print()
        print("  list [status=<status>] [priority=<priority>] [sort=<field>]")
        print("     - List tasks with optional filters")
        print("     - Status: pending, in_progress, completed, cancelled")
        print("     - Sort: created_at, updated_at, priority, due_date")
        print()
        print("  update <id> [field=value ...]")
        print("     - Update task fields (title, description, status, priority, due_date)")
        print()
        print("  delete <id>")
        print("     - Delete a task")
        print()
        print("  show <id>")
        print("     - Show detailed task information")
        print()
        print("  stats")
        print("     - Show task statistics")
        print()

