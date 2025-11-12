"""
Configuration settings for the task management system.
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "Task Manager CLI"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A command-line task management system"

# Storage settings
DEFAULT_STORAGE_FILE = "tasks.json"
STORAGE_DIR = Path.home() / ".task_manager"

# Task settings
DEFAULT_PRIORITY = "medium"
DEFAULT_STATUS = "pending"
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Display settings
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ensure storage directory exists
STORAGE_DIR.mkdir(exist_ok=True)

# Get storage file path
STORAGE_FILE = STORAGE_DIR / DEFAULT_STORAGE_FILE

