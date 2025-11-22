"""
In-memory database for projects and tasks.
"""
from core.exceptions import ProjectNotFoundError, TaskNotFoundError, DuplicateProjectNameError

from typing import Dict, List, Optional

from core.models import Project, Task

# In-memory storage
projects_db: Dict[str, Project] = {}
tasks_db: Dict[str, List[Task]] = {}  # key: project name, value: list of tasks


def is_project_name_existing(name: str) -> bool:
    """Check if a project name already exists in the database.
    :param name: The project name to check.
    :return: True if the name exists, False otherwise.
    """
    return name in projects_db


def add_project(project: Project) -> None:
    """
    Add a new project to the database.
    :param project:
    :return:
    """
    if is_project_name_existing(project.get_name()):
        raise DuplicateProjectNameError(f"Project with name '{project.get_name()}' already exists.")
    projects_db[project.get_name()] = project
    tasks_db[project.get_name()] = []


def get_project(name: str) -> Optional[Project]:
    """
    Retrieve a project by its name.
    :param name:
    :return:
    """
    project = projects_db.get(name, None)

    if project is None:
        raise ProjectNotFoundError(f"Project with name '{name}' not found.")

    return project


def get_projects() -> List[Project]:
    """
    Retrieve all projects from the database.
    :return:
    """
    return list(projects_db.values())


def update_project_name(old_name: str, updated_project:Project) -> None:
    """
    Update an existing project's name and details.
    :param old_name:
    :param updated_project:
    :return:
    """
    project: Optional[Project] = projects_db.pop(old_name, None)

    if project is None:
        raise ProjectNotFoundError(f"Project with name '{old_name}' not found.")
    
    projects_db[updated_project.get_name()] = updated_project
    tasks_db[updated_project.get_name()] = tasks_db.pop(old_name)


def delete_project(name: str) -> None:
    """
    Delete a project and all its associated tasks from the database.
    :param name:
    :return:
    """
    project: Optional[Project] = projects_db.pop(name, None)

    if project is None:
        raise ProjectNotFoundError(f"Project with name '{name}' not found.")

    tasks_db.pop(name, None)


def add_task(project_name: str, task: Task) -> None:
    """
    Add a new task to a specific project.
    :param project_name:
    :param task:
    :return:
    """
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    tasks_db[project_name].append(task)


def get_tasks(project_name: str) -> List[Task]:
    """
    Retrieve all tasks for a specific project.
    :param project_name:
    :return:
    """
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    return tasks_db.get(project_name, [])


def get_task_by_uuid(project_name: str, task_uuid: str) -> Task:
    """
    Retrieve a task by its UUID within a specific project.
    :param project_name:
    :param task_uuid:
    :return:
    """
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    for task in tasks_db[project_name]:
        if task.get_uuid() == task_uuid:
            return task
    raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")


def update_task_by_uuid(project_name: str, task_uuid: str, updated_task: Task) -> None:
    """
    Update a task by its UUID within a specific project.
    :param project_name:
    :param task_uuid:
    :param updated_task:
    :return:
    """
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    for idx, task in enumerate(tasks_db[project_name]):
        if task.get_uuid() == task_uuid:
            tasks_db[project_name][idx] = updated_task
            return
    raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")


def delete_task_by_uuid(project_name: str, task_uuid: str) -> None:
    """
    Delete a task by its UUID within a specific project.
    :param project_name:
    :param task_uuid:
    :return:
    """
    if project_name not in tasks_db:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")

    original_length = len(tasks_db[project_name])
    tasks_db[project_name] = [t for t in tasks_db[project_name] if t.get_uuid() != task_uuid]

    if len(tasks_db[project_name]) == original_length:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project_name}'.")
