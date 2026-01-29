from pydantic import BaseModel, Field
from typing import Optional


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: str = Field(..., min_length=1, max_length=100)


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class TargetResponse(TargetBase):
    id: int
    mission_id: int
    notes: str
    is_completed: bool

    model_config = {"from_attributes": True}
