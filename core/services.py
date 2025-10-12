from data.in_memory_db import (
    add_project, get_project, update_project_name, delete_project as db_delete_project
)

from core.models import Project


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
