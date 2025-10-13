# TodoList

A todo list application for managing projects and tasks efficiently.

## Features

-  **Project Management**: Create, update, delete, and list projects
-  **Task Management**: Add, update, delete, and list tasks within projects
-  **Task Status Tracking**: Track tasks with three states (todo, doing, done)
-  **Deadline Support**: Set optional deadlines for tasks

## Requirements

- Python 3.13 or higher
- Poetry (for dependency management)

## Installation

### 1. Install Poetry

If you don't have Poetry installed, install it by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).

### 2. Clone the Repository

```bash
git clone https://github.com/MKmasterg/todolist.git
cd todolist
```

### 3. Install Dependencies

```bash
poetry install
```

This will create a virtual environment and install all required dependencies specified in `pyproject.toml`.

## Running the Application

### Using Poetry

```bash
poetry run python main.py
```

## Usage

Once the application starts, you'll see a welcome message and a command prompt (`>`). Here are the available commands:

### Project Commands

**List all projects:**
```
get projects
```

**Add a new project:**
```
add project
```
You'll be prompted to enter:
- Project name (max 30 characters)
- Project description (max 150 characters)

**Update a project:**
```
update project "<project-name>"
```
You'll be prompted to enter new values for:
- Project name (leave blank to keep unchanged)
- Project description (leave blank to keep unchanged)

**Delete a project:**
```
delete project "<project-name>"
```

### Task Commands

**List all tasks in a project:**
```
get tasks "<project-name>"
```

**Add a new task:**
```
add task
```
You'll be prompted to enter:
- Project name to add the task to
- Task title (max 30 characters)
- Task description (max 150 characters)
- Task status (todo, doing, or done) - default: todo
- Task deadline (YYYY-MM-DD format, optional)

**Update a task:**
```
update task "<project-name>" <task-id>
```
You'll be prompted to update:
- Task title (leave blank to keep unchanged)
- Task description (leave blank to keep unchanged)
- Task status (leave blank to keep unchanged)
- Task deadline (leave blank to keep unchanged)

**Update only a task's status:**
```
update task_status "<project-name>" <task-id> <new-status>
```
Where `<new-status>` is one of: `todo`, `doing`, or `done`

**Delete a task:**
```
delete task "<project-name>" <task-id>
```

## Project Structure

```
todolist/
├── core/               # Core business logic
│   ├── exceptions.py   # Custom exceptions
│   ├── models.py       # Data models (Project, Task, Status)
│   └── services.py     # Business logic services
├── data/               # Data layer
│   ├── env_loader.py   # Environment configuration
│   └── in_memory_db.py # In-memory database implementation
├── interface/          # User interface layer
│   ├── arg_parser.py   # Command argument parser
│   └── cli.py          # CLI command handlers
├── utils/              # Utility functions
│   ├── id_generator.py # Unique ID generation
│   └── validators.py   # Input validation
├── main.py             # Application entry point
└── pyproject.toml      # Poetry configuration
```

## Configuration

You can configure the application by creating a `.env` file in the root directory:

```env
MAX_NUMBER_OF_PROJECT=100
MAX_NUMBER_OF_TASK=1000
```

## Development

### Adding New Dependencies

```bash
poetry add <package-name>
```

### Adding Development Dependencies

```bash
poetry add --group dev <package-name>
```

### Updating Dependencies

```bash
poetry update
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
