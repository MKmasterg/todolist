from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime
from core.validators.task_validators import (
    validate_task_title, 
    validate_task_description, 
    validate_task_status, 
    validate_task_deadline
)

class TaskCreateRequest(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    deadline: Optional[Union[datetime, str]] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        validate_task_title(v)
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_task_description(v)
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_task_status(v)
        return v
        
    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v: Optional[Union[datetime, str]]) -> Optional[Union[datetime, str]]:
        validate_task_deadline(v)
        return v

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[Union[datetime, str]] = None
    project_id: Optional[int] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_task_title(v)
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_task_description(v)
        return v

    @field_validator('status')
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_task_status(v)
        return v

    @field_validator('deadline')
    @classmethod
    def validate_deadline(cls, v: Optional[Union[datetime, str]]) -> Optional[Union[datetime, str]]:
        if v is not None:
             validate_task_deadline(v)
        return v
