from pydantic import BaseModel, field_validator
from typing import Optional
from core.validators.project_validators import validate_project_name, validate_project_description

class ProjectCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        validate_project_name(v)
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_project_description(v)
        return v

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_project_name(v)
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            validate_project_description(v)
        return v
