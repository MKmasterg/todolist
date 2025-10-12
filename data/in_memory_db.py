"""
In-memory database for projects and tasks.
"""
from core.exceptions import ProjectNotFoundError

from typing import Dict, List

from core.models import Project, Task

# In-memory storage
projects_db: Dict[str, Project] = {}
tasks_db: Dict[str, List[Task]] = {}  # key: project name, value: list of tasks

def add_project(project: Project) -> None:
    projects_db[project.name] = project
    tasks_db[project.name] = []

def get_project(name: str) -> Project:
    project: Project = projects_db.get(name, None)
    if project is None:
        raise ProjectNotFoundError(f"Project with name '{name}' not found.")
    return project

def update_project_name(old_name: str, new_name: str) -> None:
    project: Project = projects_db.pop(old_name, None)

    if project is None:
        raise ProjectNotFoundError(f"Project with name '{old_name}' not found.")

    project.name = new_name
    projects_db[new_name] = project
    tasks_db[new_name] = tasks_db.pop(old_name)

def delete_project(name: str) -> None:
    project: Project = projects_db.pop(name, None)

    if project is None:
        raise ProjectNotFoundError(f"Project with name '{name}' not found.")

    tasks_db.pop(name, None)

def add_task(project_name: str, task: Task) -> None:
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    tasks_db[project_name].append(task)

def get_tasks(project_name: str) -> List[Task]:
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    return tasks_db.get(project_name, [])

def delete_task(project_name: str, task: Task) -> None:
    if project_name in tasks_db:
        tasks_db[project_name] = [t for t in tasks_db[project_name] if t != task]
    else:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")

