# TodoList

A todo list application for managing projects and tasks efficiently.

## Features

-  **Project Management**: Create, update, delete, and list projects
-  **Task Management**: Add, update, delete, and list tasks within projects
-  **Task Status Tracking**: Track tasks with three states (todo, doing, done)
-  **Deadline Support**: Set optional deadlines for tasks
-  **Automated Task Closure**: Background scheduler to automatically close overdue tasks
-  **PostgreSQL Database**: Persistent storage using PostgreSQL
-  **Database Migrations**: Alembic integration for schema management

## Requirements

- Python 3.13 or higher
- Poetry (for dependency management)
- Docker and Docker Compose (for PostgreSQL database)

## Installation

### 1. Install Docker

Make sure you have Docker Desktop installed on Windows. Download it from [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).

### 2. Install Poetry

If you don't have Poetry installed, install it by following the instructions at [https://python-poetry.org/docs/#installation](https://www.python-poetry.org/docs/#installation).

### 3. Clone the Repository

```bash
git clone https://github.com/MKmasterg/todolist.git
cd todolist
```

### 4. Install Dependencies

```bash
poetry install
```

### 5. Set Up Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
cp .env.example .env
```

Or manually create a `.env` file with the following content:

```env
# Application Configuration
MAX_NUMBER_OF_PROJECT=1000
MAX_NUMBER_OF_TASK=10000

# PostgreSQL Database Configuration
POSTGRES_USER=todolist
POSTGRES_PASSWORD=todolist123
POSTGRES_DB=todolist_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Database URL
DATABASE_URL=postgresql://todolist:todolist123@localhost:5432/todolist_db
```

### 6. Start PostgreSQL with Docker Compose

```bash
docker compose -f docker-compose.yml up -d
```

This will start a PostgreSQL database container in the background.

### 7. Run Database Migrations

```bash
poetry run alembic upgrade head
```

This will create the necessary database tables.
## Running the Application

### Using Poetry

```bash
poetry run python main.py
```
## Usage

> **⚠️ CLI Deprecation Notice:**
> The command-line interface (CLI) is deprecated and will be removed in future versions. Please use the RESTful API for all interactions. See below for API usage instructions.


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
│   ├── models.py       # Domain models (Project, Task, Status)
│   ├── services.py     # Business logic services
│   └── validators/     # Input validators
│       ├── project_validators.py
│       └── task_validators.py
├── data/               # Data layer
│   ├── database.py     # Database connection and session management
│   ├── env_loader.py   # Environment configuration
│   ├── models/         # SQLAlchemy ORM models
│   │   ├── project_model.py
│   │   └── task_model.py
│   ├── repositories/   # Data access layer
│   │   ├── base.py
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   └── migrations/     # Alembic database migrations
│       └── versions/
├── interface/          # User interface layer
|    |── cli/              # Command-line interface (deprecated)
|    |   |
│    |   ├── arg_parser.py   # Command argument parser
│    |   └── cli.py          # CLI command handlers
│    └── api/              # RESTful API interface
├── utils/              # Utility functions
│   └── id_generator.py # Unique ID generation
├── main.py             # Application entry point
├── pyproject.toml      # Poetry configuration
├── alembic.ini         # Alembic configuration
└── docker-compose.yml  # Docker Compose for PostgreSQL
```

## Configuration

You can configure the application by creating a `.env` file in the root directory:

```env
# Application Configuration
MAX_NUMBER_OF_PROJECT=1000
MAX_NUMBER_OF_TASK=10000

# PostgreSQL Database Configuration
POSTGRES_USER=todolist
POSTGRES_PASSWORD=todolist123
POSTGRES_DB=todolist_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Database URL
DATABASE_URL=postgresql://todolist:todolist123@localhost:5432/todolist_db
```

### Configuration Options

- `MAX_NUMBER_OF_PROJECT`: Maximum number of projects (default: 1000)
- `MAX_NUMBER_OF_TASK`: Maximum number of tasks (default: 10000)
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_HOST`: PostgreSQL host (default: localhost)
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `DATABASE_URL`: Full database connection URL

## Development

### Database Migrations

Create a new migration after modifying models:

```bash
poetry run alembic revision --autogenerate -m "description of changes"
```

Apply migrations:

```bash
poetry run alembic upgrade head
```

Rollback last migration:

```bash
poetry run alembic downgrade -1
```

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

## Background Scheduler

The application includes a background scheduler that automatically closes overdue tasks.

### Quick Start

Run the scheduler in the background:

```bash
# Default: runs every 15 minutes
poetry run python scheduler.py

# Custom interval (in minutes)
poetry run python scheduler.py --interval 30
```

### Manual Trigger

You can also manually trigger the auto-close job from the CLI:

```
> tasks:autoclose-overdue
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
