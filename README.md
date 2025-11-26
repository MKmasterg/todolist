# TodoList

A todo list application for managing projects and tasks efficiently.

## Features

-  **RESTful API**: Full-featured API for integration with other tools
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

Make sure you have Docker Desktop installed on Windows/Mac or Docker Engine on Linux.

### 2. Install Poetry

If you don't have Poetry installed, install it by following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).

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
PORT=8000

# PostgreSQL Database Configuration
POSTGRES_USER=todolist
POSTGRES_PASSWORD=[REDACTED:password]
POSTGRES_DB=todolist_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Database URL
DATABASE_URL=postgresql+asyncpg://todolist:todolist123@localhost:5432/todolist_db
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

### API Server (Recommended)

To start the RESTful API server:

```bash
poetry run python main.py
```

The API will be available at `http://localhost:8000` (or the port specified in your `.env`).

**Interactive Documentation:**
Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Background Scheduler

Run the scheduler in the background to automatically close overdue tasks:

```bash
# Default: runs every 15 minutes
poetry run python scheduler.py

# Custom interval (in minutes)
poetry run python scheduler.py --interval 30
```

Note: The scheduler runs an initial check immediately upon starting.

## API Usage

All API endpoints are prefixed with `/api/v1`.

### Projects

- `GET /api/v1/projects/`: List all projects
- `POST /api/v1/projects/`: Create a new project
- `GET /api/v1/projects/{project_name}`: Get project details
- `PUT /api/v1/projects/{project_name}`: Update a project
- `DELETE /api/v1/projects/{project_name}`: Delete a project

### Tasks

- `GET /api/v1/projects/{project_name}/tasks/`: List tasks in a project
- `POST /api/v1/projects/{project_name}/tasks/`: Create a new task
- `GET /api/v1/projects/{project_name}/tasks/{task_uuid}`: Get task details
- `PUT /api/v1/projects/{project_name}/tasks/{task_uuid}`: Update a task
- `DELETE /api/v1/projects/{project_name}/tasks/{task_uuid}`: Delete a task

## Configuration Options

You can configure the application variables in your `.env` file:

- `MAX_NUMBER_OF_PROJECT`: Maximum number of projects (default: 1000)
- `MAX_NUMBER_OF_TASK`: Maximum number of tasks (default: 10000)
- `PORT`: Port for the API server (default: 8000)
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: PostgreSQL database name
- `POSTGRES_HOST`: PostgreSQL host (default: localhost)
- `POSTGRES_PORT`: PostgreSQL port (default: 5432)
- `DATABASE_URL`: Full database connection URL

## Project Structure

```
todolist/
├── core/               # Core business logic
│   ├── exceptions.py   # Custom exceptions
│   ├── models.py       # Domain models (Project, Task, Status)
│   ├── services.py     # Business logic services
│   └── validators/     # Input validators
├── data/               # Data layer
│   ├── database.py     # Database connection and session management
│   ├── env_loader.py   # Environment configuration
│   ├── models/         # SQLAlchemy ORM models
│   ├── repositories/   # Data access layer
│   └── migrations/     # Alembic database migrations
├── interface/          # User interface layer
│   └── api/            # RESTful API
│       ├── controller_schemas/  # Pydantic schemas for requests/responses
│       ├── controllers/         # API controllers
│       └── routers.py           # API route definitions
├── utils/              # Utility functions
├── main.py             # API entry point
├── scheduler.py        # Background scheduler entry point
├── pyproject.toml      # Poetry configuration
├── alembic.ini         # Alembic configuration
└── docker-compose.yml  # Docker Compose for PostgreSQL
```

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

### Managing Dependencies

Add a new dependency:
```bash
poetry add <package-name>
```

Add a development dependency:
```bash
poetry add --group dev <package-name>
```

Update dependencies:
```bash
poetry update
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
