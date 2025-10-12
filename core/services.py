from typing import Optional, List

from data.in_memory_db import (
    add_project, get_project, update_project_name, delete_project as db_delete_project,
    add_task, get_tasks, get_task_by_uuid, update_task_by_uuid, delete_task_by_uuid
)

from core.models import Project, Status, Task

from datetime import datetime


def is_project_name_existing(name: str) -> bool:
    """Check if a project name already exists in the database.
    :param name: The project name to check.
    :return: True if the name exists, False otherwise.
    """

    return get_project(name) is not None


def create_project(project: Project) -> bool:
    """Create a new project in the database.
    :param project: The Project instance to create.
    :return: True if the project was created successfully.
    """
    add_project(project)
    return True


def update_project(old_project: Project, new_name: str, new_desc: str) -> bool:
    """Update an existing project in the database.
    :param old_project: The existing Project instance to update.
    :param new_name: The new Project name.
    :param new_desc: The new Project description.
    :return: True if the project was updated successfully.
    """
    new_project = Project(name=new_name, description=new_desc)
    update_project_name(old_project.name, new_project.name)
    return True


def delete_project(project: Project) -> bool:
    """Delete a project from the database with all its associated tasks.
    :param project: The Project instance to delete.
    :return: True if the project was deleted successfully.
    """
    db_delete_project(project.name)
    return True


def add_task_to_project(project: Project, title: str, description: str = "", status: str = Status.TODO,
                        deadline: Optional[datetime] = None) -> bool:
    """Add a task to a project in the database.
    :param project: The Project instance to which the task will be added.
    :param title: The task title.
    :param description: The task description.
    :param status: The task status (todo, doing, or done) - defaults to 'todo'
    :param deadline: Optional task deadline
    :return: True if the task was added successfully.
    """
    task = Task(title=title, description=description, status=status, deadline=deadline)
    add_task(project.name, task)
    return True


def update_task_status(project: Project, task_uuid: str, new_status: str) -> bool:
    """
    Update the status of a task.

    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to update.
    :param new_status: The new status (must be one of: todo, doing, done).
    :return: True if the task status was updated successfully.
    """
    task = get_task_by_uuid(project.name, task_uuid)
    task.set_status(new_status)
    update_task_by_uuid(project.name, task_uuid, task)
    return True


def update_task_elements(project: Project, task_uuid: str, new_title: str, new_description: str = "",
                new_status: str = Status.TODO, new_deadline: Optional[datetime] = None) -> bool:
    """
    Update the details of a task.

    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to update.
    :param new_title: The new task title.
    :param new_description: The new task description.
    :param new_status: The new task status (must be one of: todo, doing, done).
    :param new_deadline: The new task deadline (must be a valid date or None).
    :return: True if the task was updated successfully.
    """
    task = get_task_by_uuid(project.name, task_uuid)
    new_task = Task(title=new_title, description=new_description, status=new_status, deadline=new_deadline)
    # Preserve the original uuid
    new_task.uuid = task.uuid
    update_task_by_uuid(project.name, task_uuid, new_task)
    return True


def delete_task_from_project(project: Project, task_uuid: str) -> bool:
    """
    Delete a task from a project.

    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to delete.
    :return: True if the task was deleted successfully.
    """
    delete_task_by_uuid(project.name, task_uuid)
    return True


def get_project_tasks(project: Project) -> List[Task]:
    """
    Get all tasks for a project.

    :param project: The Project instance.
    :return: List of tasks in the project.
    """
    return get_tasks(project.name)
