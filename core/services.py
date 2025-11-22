from typing import Optional, List, cast
from datetime import datetime

from sqlalchemy.orm import Session

from data.repositories.project_repository import ProjectRepository
from data.repositories.task_repository import TaskRepository
from core.models import Project, Status, Task
from core.validators.task_validators import (
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_task_deadline
)
from core.validators.project_validators import (
    validate_project_name,
    validate_project_description
)
from core.exceptions import ProjectNotFoundError, TaskNotFoundError


def get_project_from_name(db: Session, name: str) -> Optional[Project]:
    """Retrieve a project by its name.
    :param db: Database session.
    :param name: The project name to search for.
    :return: The Project instance if found, None otherwise.
    """
    validate_project_name(name)
    
    repo = ProjectRepository(db)
    project_model = repo.get_by_name(name)
    if not project_model:
        return None
    
    # Convert ProjectModel to Project domain model
    project = Project(name=project_model.name, description=project_model.description or "")
    return project


def create_project(db: Session, name: str, desc: str) -> bool:
    """Create a new project in the database.
    :param db: Database session.
    :param name: The Project name.
    :param desc: The Project description.
    :return: True if the project was created successfully.
    """
    validate_project_name(name)
    validate_project_description(desc)
    
    repo = ProjectRepository(db)
    repo.create_project(name, desc)
    db.commit()
    return True


def update_project(db: Session, old_name: str, updated_project: Project) -> bool:
    """Update an existing project in the database.
    :param db: Database session.
    :param old_name: The current name of the project to update.
    :param updated_project: The Project instance with updated details.
    :return: True if the project was updated successfully.
    """
    validate_project_name(old_name)
    validate_project_name(updated_project.get_name())
    validate_project_description(updated_project.get_description())
    
    repo = ProjectRepository(db)
    repo.update_project(old_name, updated_project.get_name(), updated_project.get_description())
    db.commit()
    return True


def delete_project(db: Session, project: Project) -> bool:
    """Delete a project from the database with all its associated tasks.
    :param db: Database session.
    :param project: The Project instance to delete.
    :return: True if the project was deleted successfully.
    """
    validate_project_name(project.get_name())
    
    repo = ProjectRepository(db)
    repo.delete_project(project.get_name())
    db.commit()
    return True


def get_task_by_uuid_in_project(db: Session, project_name: str, task_uuid: str) -> Optional[Task]:
    """Retrieve a task by its UUID within a specific project.
    :param db: Database session.
    :param project_name: The name of the project containing the task.
    :param task_uuid: The UUID of the task to search for.
    :return: The Task instance if found, None otherwise.
    """
    validate_project_name(project_name)
    
    # First verify the project exists
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project_name)
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    
    # Get task by UUID
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    
    if not task_model or task_model.project_id != project_model.id:
        return None
    
    # Convert TaskModel to Task domain model
    task_desc = task_model.description if task_model.description is not None else ""
    task = Task(
        title=task_model.title,
        description=task_desc,
        status=task_model.status,
        deadline=task_model.deadline
    )
    task.uuid = str(task_model.uuid)
    return task


def add_task_to_project(db: Session, project: Project, title: str, description: str = "", 
                        status: str = Status.TODO, deadline: Optional[datetime] = None) -> bool:
    """Add a task to a project in the database.
    :param db: Database session.
    :param project: The Project instance to which the task will be added.
    :param title: The task title.
    :param description: The task description.
    :param status: The task status (todo, doing, or done) - defaults to 'todo'
    :param deadline: Optional task deadline
    :return: True if the task was added successfully.
    """
    validate_project_name(project.get_name())
    validate_task_title(title)
    validate_task_description(description)
    validate_task_status(status)
    if deadline is not None:
        validate_task_deadline(deadline)
    
    # Get project from database
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    
    # Create task
    task_repo = TaskRepository(db)
    task_repo.create_task(
        project_id=project_model.id,
        title=title,
        description=description,
        status=status,
        deadline=deadline
    )
    db.commit()
    return True


def update_task_status(db: Session, project: Project, task_uuid: str, new_status: str) -> bool:
    """
    Update the status of a task.

    :param db: Database session.
    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to update.
    :param new_status: The new status (must be one of: todo, doing, done).
    :return: True if the task status was updated successfully.
    """
    validate_project_name(project.get_name())
    validate_task_status(new_status)
    
    # Verify project exists
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    
    # Get and update task
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
    
    # Update only the status
    task_desc = task_model.description if task_model.description is not None else ""
    task_repo.update_task(
        uuid=task_uuid,
        title=task_model.title,
        description=task_desc,
        status=new_status,
        deadline=task_model.deadline
    )
    db.commit()
    return True


def update_task_elements(db: Session, project: Project, task_uuid: str, new_title: str, 
                         new_description: str = "", new_status: str = Status.TODO, 
                         new_deadline: Optional[datetime] = None) -> bool:
    """
    Update the details of a task.

    :param db: Database session.
    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to update.
    :param new_title: The new task title.
    :param new_description: The new task description.
    :param new_status: The new task status (must be one of: todo, doing, done).
    :param new_deadline: The new task deadline (must be a valid date or None).
    :return: True if the task was updated successfully.
    """
    validate_project_name(project.get_name())
    validate_task_title(new_title)
    validate_task_description(new_description)
    validate_task_status(new_status)
    if new_deadline is not None:
        validate_task_deadline(new_deadline)
    
    # Verify project exists
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    
    # Get and update task
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")    
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
    
    # Update task with new values
    task_repo.update_task(
        uuid=task_uuid,
        title=new_title,
        description=new_description,
        status=new_status,
        deadline=new_deadline
    )
    db.commit()
    return True


def delete_task_from_project(db: Session, project: Project, task_uuid: str) -> bool:
    """
    Delete a task from a project.

    :param db: Database session.
    :param project: The Project instance containing the task.
    :param task_uuid: The UUID of the task to delete.
    :return: True if the task was deleted successfully.
    """
    validate_project_name(project.get_name())
    
    # Verify project exists
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    
    # Verify task exists and belongs to project
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")
    
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
    
    # Delete task
    task_repo.delete_task(task_uuid)
    db.commit()
    return True


def get_project_list(db: Session) -> List[Project]:
    """
    Get all projects.

    :param db: Database session.
    :return: List of all projects.
    """
    repo = ProjectRepository(db)
    project_models = repo.get_all_projects()
    
    # Convert ProjectModels to Project domain models
    projects = []
    for pm in project_models:
        project = Project(name=pm.name, description=pm.description or "")
        projects.append(project)
    
    return projects


def get_project_tasks(db: Session, project: Project) -> List[Task]:
    """
    Get all tasks for a project.

    :param db: Database session.
    :param project: The Project instance.
    :return: List of tasks in the project.
    """
    validate_project_name(project.get_name())
    
    # Get project from database
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    
    # Get all tasks for the project
    task_repo = TaskRepository(db)
    task_models = task_repo.get_tasks_by_project(project_model.id)
    
    # Convert TaskModels to Task domain models
    tasks = []
    for tm in task_models:
        task_desc = tm.description if tm.description is not None else ""
        task = Task(
            title=tm.title,
            description=task_desc,
            status=tm.status,
            deadline=tm.deadline
        )
        task.uuid = str(tm.uuid)
        tasks.append(task)
    
    return tasks
