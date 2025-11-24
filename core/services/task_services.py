# Task-related service functions

from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from core.models import Task, Status, Project
from data.repositories.task_repository import TaskRepository
from data.repositories.project_repository import ProjectRepository
from core.validators.task_validators import (
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_task_deadline
)
from core.exceptions import ProjectNotFoundError, TaskNotFoundError


def get_task_by_uuid_in_project(db: Session, project_name: str, task_uuid: str) -> Optional[Task]:
    validate_project_name = lambda name: None  # Assume already validated in project_services
    validate_project_name(project_name)
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project_name)
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project_name}' not found.")
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model or task_model.project_id != project_model.id:
        return None
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
    validate_project_name = lambda name: None  # Assume already validated in project_services
    validate_project_name(project.get_name())
    validate_task_title(title)
    validate_task_description(description)
    validate_task_status(status)
    if deadline is not None:
        validate_task_deadline(deadline)
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
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
    validate_project_name = lambda name: None
    validate_project_name(project.get_name())
    validate_task_status(new_status)
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
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
    validate_project_name = lambda name: None
    validate_project_name(project.get_name())
    validate_task_title(new_title)
    validate_task_description(new_description)
    validate_task_status(new_status)
    if new_deadline is not None:
        validate_task_deadline(new_deadline)
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")    
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
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
    validate_project_name = lambda name: None
    validate_project_name(project.get_name())
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    task_repo = TaskRepository(db)
    task_model = task_repo.get_by_uuid(task_uuid)
    if not task_model:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found.")
    if task_model.project_id != project_model.id:
        raise TaskNotFoundError(f"Task with uuid '{task_uuid}' not found in project '{project.get_name()}'.")
    task_repo.delete_task(task_uuid)
    db.commit()
    return True


def get_project_tasks(db: Session, project: Project) -> List[Task]:
    validate_project_name = lambda name: None
    validate_project_name(project.get_name())
    project_repo = ProjectRepository(db)
    project_model = project_repo.get_by_name(project.get_name())
    if not project_model:
        raise ProjectNotFoundError(f"Project with name '{project.get_name()}' not found.")
    task_repo = TaskRepository(db)
    task_models = task_repo.get_tasks_by_project(project_model.id)
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
