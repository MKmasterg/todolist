from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from data.database import get_db
from interface.api.controller_schemas import requests, responses as schemas
from core.services import project_services, task_services
from core.models import Project
from core.exceptions import (
    ProjectNotFoundError, 
    TaskNotFoundError, 
    MaxProjectsReachedError, 
    MaxTasksReachedError
)

router = APIRouter()

# --- Projects ---

@router.get("/projects/", response_model=List[schemas.ProjectResponse])
async def read_projects(db: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of all projects.
    
    Returns:
        List[ProjectResponse]: A list of all projects.
    """
    projects = await project_services.get_project_list(db)
    return projects

@router.post("/projects/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: schemas.ProjectCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new project.
    
    Args:
        project (ProjectCreate): The project creation data.
        db (AsyncSession): Database session.
        
    Returns:
        ProjectResponse: The created project.
        
    Raises:
        HTTPException: If project limit reached or validation fails.
    """
    try:
        await project_services.create_project(db, project.name, project.description)
        # Return the created project object
        return schemas.ProjectResponse(name=project.name, description=project.description)
    except MaxProjectsReachedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e: # For validation errors
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/projects/{project_name}", response_model=schemas.ProjectResponse)
async def read_project(project_name: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific project by name.
    
    Args:
        project_name (str): The name of the project.
        db (AsyncSession): Database session.
        
    Returns:
        ProjectResponse: The project details.
        
    Raises:
        HTTPException: If project not found.
    """
    try:
        project = await project_services.get_project_from_name(db, project_name)
        if not project:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        return project
    except ValueError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/projects/{project_name}", response_model=schemas.ProjectResponse)
async def update_project(project_name: str, project_update: schemas.ProjectUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a project's description.
    
    Args:
        project_name (str): The name of the project to update.
        project_update (ProjectUpdate): The new project data (only description for now).
        db (AsyncSession): Database session.
        
    Returns:
        ProjectResponse: The updated project.
        
    Raises:
        HTTPException: If project not found or validation fails.
    """
    try:
        # First check if project exists and get it
        existing_project = await project_services.get_project_from_name(db, project_name)
        if not existing_project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        # Determine new values (keep old if not provided)
        new_description = project_update.description if project_update.description is not None else existing_project.description
        # Note: schemas.ProjectUpdate doesn't allow changing name currently, based on the current business logic. 

        updated_project_model = Project(name=project_name, description=new_description)
        
        await project_services.update_project(db, project_name, updated_project_model)
        
        return schemas.ProjectResponse(name=project_name, description=new_description)

    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/projects/{project_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_name: str, db: AsyncSession = Depends(get_db)):
    """
    Delete a project by name.
    
    Args:
        project_name (str): The name of the project to delete.
        db (AsyncSession): Database session.
        
    Returns:
        Response: 204 No Content on success.
        
    Raises:
        HTTPException: If project not found.
    """
    try:
        # First check if it exists
        existing_project = await project_services.get_project_from_name(db, project_name)
        if not existing_project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        
        await project_services.delete_project(db, existing_project)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# --- Tasks ---

@router.get("/projects/{project_name}/tasks/", response_model=List[schemas.TaskResponse])
async def read_tasks(project_name: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all tasks for a given project.
    
    Args:
        project_name (str): The name of the project.
        db (AsyncSession): Database session.
        
    Returns:
        List[TaskResponse]: A list of tasks in the project.
        
    Raises:
        HTTPException: If project not found.
    """
    try:
        # Construct a temporary project object to pass to the service
        # The service mainly uses it for get_name()
        project = Project(name=project_name) 
        tasks = await task_services.get_project_tasks(db, project)
        return tasks
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/projects/{project_name}/tasks/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(project_name: str, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new task in a project.
    
    Args:
        project_name (str): The name of the project.
        task (TaskCreate): The task creation data.
        db (AsyncSession): Database session.
        
    Returns:
        TaskResponse: The created task.
        
    Raises:
        HTTPException: If task limit reached, project not found, or validation fails.
    """
    try:
        project = Project(name=project_name)
        created_task = await task_services.add_task_to_project(
            db, 
            project, 
            task.title, 
            task.description, 
            task.status, 
            task.deadline
        )
        return created_task
    except MaxTasksReachedError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) 

@router.get("/projects/{project_name}/tasks/{task_uuid}", response_model=schemas.TaskResponse)
async def read_task(project_name: str, task_uuid: str, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a specific task by UUID within a project.
    
    Args:
        project_name (str): The name of the project.
        task_uuid (str): The UUID of the task.
        db (AsyncSession): Database session.
        
    Returns:
        TaskResponse: The task details.
        
    Raises:
        HTTPException: If task or project not found.
    """
    try:
        task = await task_services.get_task_by_uuid_in_project(db, project_name, task_uuid)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return task
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/projects/{project_name}/tasks/{task_uuid}", response_model=schemas.TaskResponse)
async def update_task(project_name: str, task_uuid: str, task_update: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a task's details.
    
    Args:
        project_name (str): The name of the project.
        task_uuid (str): The UUID of the task.
        task_update (TaskUpdate): The new task data (fields set to None are ignored).
        db (AsyncSession): Database session.
        
    Returns:
        TaskResponse: The updated task.
        
    Raises:
        HTTPException: If task/project not found or validation fails.
    """
    try:
        project = Project(name=project_name)
        
        # We need to fetch the current task to handle partial updates if fields are None
        current_task = await task_services.get_task_by_uuid_in_project(db, project_name, task_uuid)
        if not current_task:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
             
        new_title = task_update.title if task_update.title is not None else current_task.title
        new_desc = task_update.description if task_update.description is not None else current_task.description
        new_status = task_update.status if task_update.status is not None else current_task.status
        new_deadline = task_update.deadline if task_update.deadline is not None else current_task.deadline

        await task_services.update_task_elements(
            db, 
            project, 
            task_uuid, 
            new_title, 
            new_desc, 
            new_status, 
            new_deadline
        )
        
        # Construct response
        return schemas.TaskResponse(
            uuid=task_uuid,
            title=new_title,
            description=new_desc,
            status=new_status,
            deadline=new_deadline
        )

    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/projects/{project_name}/tasks/{task_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(project_name: str, task_uuid: str, db: AsyncSession = Depends(get_db)):
    """
    Delete a task from a project.
    
    Args:
        project_name (str): The name of the project.
        task_uuid (str): The UUID of the task to delete.
        db (AsyncSession): Database session.
        
    Returns:
        Response: 204 No Content on success.
        
    Raises:
        HTTPException: If task or project not found.
    """
    try:
        project = Project(name=project_name)
        await task_services.delete_task_from_project(db, project, task_uuid)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProjectNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
