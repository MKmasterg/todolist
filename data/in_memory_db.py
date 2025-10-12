"""
In-memory database for projects and tasks.
"""
from core.exceptions import ProjectNotFoundError, TaskNotFoundError

from typing import Dict, List, Optional

from core.models import Project, Task

# In-memory storage
projects_db: Dict[str, Project] = {}
tasks_db: Dict[str, List[Task]] = {}  # key: project name, value: list of tasks


def add_project(project: Project) -> None:
    projects_db[project.name] = project
    tasks_db[project.name] = []


def get_project(name: str) -> Optional[Project]:
    return projects_db.get(name, None)


def get_projects() -> List[Project]:
    return list(projects_db.values())


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


def get_task_by_uuid(project_name: str, task_uuid: str) -> Task:
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    for task in tasks_db[project_name]:
        if task.uuid == task_uuid:
            return task
    raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")


def update_task_by_uuid(project_name: str, task_uuid: str, updated_task: Task) -> None:
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    for idx, task in enumerate(tasks_db[project_name]):
        if task.uuid == task_uuid:
            tasks_db[project_name][idx] = updated_task
            return
    raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")


def delete_task_by_uuid(project_name: str, task_uuid: str) -> None:
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")

    original_length = len(tasks_db[project_name])
    tasks_db[project_name] = [t for t in tasks_db[project_name] if t.uuid != task_uuid]

    if len(tasks_db[project_name]) == original_length:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")
