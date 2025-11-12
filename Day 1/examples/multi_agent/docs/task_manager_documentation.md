
# Task Manager CLI Documentation

## Project Overview

The Task Manager CLI is a command-line application designed to help users manage their tasks efficiently. It allows users to add, list, update, delete, and view tasks with various filtering and sorting options. The application stores task data in a JSON file for persistence.

## Architecture and Module Descriptions

The project is structured into several modules, each responsible for a specific aspect of the application:

-   **`task.py`**: Defines the core data models for tasks, including the `Task` class and enumerations for `TaskStatus` and `TaskPriority`. It also includes methods for task status checks and serialization.
-   **`config.py`**: Contains application-wide configuration settings such as storage paths, default values, and display formats.
-   **`cli.py`**: Implements the command-line interface, handling user input, parsing commands, and interacting with the `TaskManager`.
-   **`utils.py`**: Provides utility functions for date validation, text formatting, and parsing user input.
-   **`task_manager.py`**: Contains the main business logic for managing tasks. It interacts with the storage layer to perform CRUD operations, filtering, and statistics generation.
-   **`storage.py`**: Defines an abstract storage layer with a concrete implementation `FileStorage` that uses JSON files for persistence. A placeholder `DatabaseStorage` is included for future database integration.
-   **`main.py`**: The entry point of the application. It initializes the storage, task manager, and CLI, and handles command-line arguments or starts the interactive mode.
-   **`tests/`**: Directory containing unit tests for the `Task` and `TaskManager` classes.

## API Documentation

### `task.py`

#### `TaskStatus` Enum
-   `PENDING`: Task is waiting to be processed.
-   `IN_PROGRESS`: Task is currently being worked on.
-   `COMPLETED`: Task has been finished.
-   `CANCELLED`: Task has been cancelled.

#### `TaskPriority` Enum
-   `LOW`: Low priority task.
-   `MEDIUM`: Medium priority task.
-   `HIGH`: High priority task.

#### `Task` Class
-   `__init__(self, title: str, description: str = "", status: TaskStatus = TaskStatus.PENDING, priority: TaskPriority = TaskPriority.MEDIUM, due_date: Optional[str] = None, task_id: Optional[str] = None, created_at: Optional[str] = None, updated_at: Optional[str] = None)`:
    -   Initializes a new task.
    -   Parameters: `title`, `description`, `status`, `priority`, `due_date`, `task_id`, `created_at`, `updated_at`.
-   `is_overdue(self) -> bool`:
    -   Checks if the task is overdue based on its due date and status.
-   `to_dict(self) -> dict`:
    -   Converts the task object to a dictionary for serialization.
-   `from_dict(cls, data: dict) -> 'Task'`:
    -   Creates a `Task` instance from a dictionary.
-   `__str__(self) -> str`:
    -   Returns a user-friendly string representation of the task.
-   `__repr__(self) -> str`:
    -   Returns a developer-friendly string representation of the task.

### `config.py`
-   Contains constants for application name, version, storage paths, default task settings, and display formats.

### `cli.py`

#### `TaskCLI` Class
-   `__init__(self, manager: TaskManager)`:
    -   Initializes the CLI with a `TaskManager` instance.
-   `run(self)`:
    -   Starts the interactive command loop for the CLI.
-   `handle_command(self, args: List[str])`:
    -   Parses and routes commands to appropriate handlers.
-   `_handle_add(self, args: List[str])`: Handles the `add` command.
-   `_handle_list(self, args: List[str])`: Handles the `list` command with filtering and sorting.
-   `_handle_update(self, args: List[str])`: Handles the `update` command.
-   `_handle_delete(self, args: List[str])`: Handles the `delete` command.
-   `_handle_show(self, args: List[str])`: Handles the `show` command.
-   `_handle_stats(self)`: Handles the `stats` command.
-   `_handle_help(self)`: Displays help information.

### `utils.py`
-   `validate_date(date_string: str) -> bool`: Validates if a string is in `YYYY-MM-DD` format.
-   `format_date(date_string: Optional[str]) -> str`: Formats a date string for display.
-   `truncate_text(text: str, max_length: int = 50) -> str`: Truncates text to a specified maximum length.
-   `parse_priority(priority_string: str) -> Optional[str]`: Parses and validates a priority string.

### `task_manager.py`

#### `TaskManager` Class
-   `__init__(self, storage)`:
    -   Initializes the manager with a storage backend.
-   `add_task(self, title: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM, due_date: Optional[str] = None) -> Task`:
    -   Adds a new task.
-   `get_task(self, task_id: str) -> Optional[Task]`:
    -   Retrieves a task by its ID.
-   `update_task(self, task_id: str, **kwargs) -> Optional[Task]`:
    -   Updates an existing task's properties.
-   `delete_task(self, task_id: str) -> bool`:
    -   Deletes a task by its ID.
-   `list_tasks(self, status: Optional[TaskStatus] = None, priority: Optional[TaskPriority] = None, sort_by: str = "created_at") -> List[Task]`:
    -   Lists tasks with optional filtering by status and priority, and sorting.
-   `get_statistics(self) -> dict`:
    -   Calculates and returns statistics about the tasks.

### `storage.py`

#### `FileStorage` Class
-   `__init__(self, filepath: str)`:
    -   Initializes storage with a file path for JSON persistence.
-   `ensure_file_exists(self)`: Creates the JSON file if it doesn't exist.
-   `load_tasks(self) -> List[Task]`: Loads tasks from the JSON file.
-   `save_tasks(self, tasks: List[Task])`: Saves a list of tasks to the JSON file.
-   `clear(self)`: Clears all tasks from the storage file.

#### `DatabaseStorage` Class (Placeholder)
-   A placeholder class for future database integration. Methods `load_tasks` and `save_tasks` raise `NotImplementedError`.

## Usage Examples

### Running the Application

1.  **Interactive Mode**:
    ```bash
    python main.py
    ```
    This will start an interactive session where you can type commands.

2.  **Direct Command Execution**:
    ```bash
    python main.py add "Buy groceries" "Milk, Eggs, Bread" high 2023-12-31
    python main.py list status=pending priority=high
    python main.py show <task_id>
    python main.py delete <task_id>
    ```

### Common Commands

-   **Add a task**:
    `add <title> [description] [priority] [due_date]`
    Example: `add "Call mom" "Remind her about birthday" high 2024-01-15`
    (Priority can be `low`, `medium`, `high`. Due date format: `YYYY-MM-DD`)

-   **List tasks**:
    `list [status=<status>] [priority=<priority>] [sort=<field>]`
    Examples:
    `list` (lists all tasks)
    `list status=in_progress`
    `list priority=low sort=due_date`
    (Status can be `pending`, `in_progress`, `completed`, `cancelled`. Sort fields: `created_at`, `updated_at`, `priority`, `due_date`)

-   **Update a task**:
    `update <id> [field=value ...]`
    Example: `update abc123 description="Updated description" status=completed`
    (Fields: `title`, `description`, `status`, `priority`, `due_date`)

-   **Show task details**:
    `show <id>`
    Example: `show abc123`

-   **Delete a task**:
    `delete <id>`
    Example: `delete abc123`

-   **Show statistics**:
    `stats`

-   **Help**:
    `help`

## Installation and Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd task_manager
    ```

2.  **Install dependencies** (if any):
    Currently, the project only uses standard Python libraries.

3.  **Run the application**:
    Execute `main.py` as described in the "Usage Examples" section.

## Configuration Options

Configuration settings are managed in `config.py`:

-   `APP_NAME`: Name of the application.
-   `APP_VERSION`: Version of the application.
-   `APP_DESCRIPTION`: Description of the application.
-   `DEFAULT_STORAGE_FILE`: The default filename for storing task data (e.g., `tasks.json`).
-   `STORAGE_DIR`: The directory where the storage file is located (defaults to `~/.task_manager`).
-   `DEFAULT_PRIORITY`: Default priority for new tasks.
-   `DEFAULT_STATUS`: Default status for new tasks.
-   `MAX_TITLE_LENGTH`: Maximum allowed length for task titles.
-   `MAX_DESCRIPTION_LENGTH`: Maximum allowed length for task descriptions.
-   `DATE_FORMAT`: Default format for displaying dates.
-   `DATETIME_FORMAT`: Default format for displaying date and time.

The `STORAGE_DIR` is automatically created if it doesn't exist upon application startup.
