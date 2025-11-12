#!/usr/bin/env python3
"""
Main entry point for the Task Management CLI application.
"""

import sys
from cli import TaskCLI
from storage import FileStorage
from task_manager import TaskManager


def main():
    """Main function to run the task management CLI."""
    # Initialize storage and task manager
    storage = FileStorage("tasks.json")
    manager = TaskManager(storage)
    cli = TaskCLI(manager)
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        cli.handle_command(sys.argv[1:])
    else:
        cli.run()


if __name__ == "__main__":
    main()

