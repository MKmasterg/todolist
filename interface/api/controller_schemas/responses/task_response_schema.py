from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional
from datetime import datetime

class TaskResponse(BaseModel):
    uuid: UUID4
    project_id: int
    title: str
    description: Optional[str] = None
    status: str
    deadline: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
