from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

from app.schemas.target import TargetCreate, TargetResponse
from app.schemas.cat import CatResponse


class MissionCreate(BaseModel):
    targets: List[TargetCreate] = Field(..., min_length=1, max_length=3)

    @field_validator('targets')
    @classmethod
    def validate_targets_count(cls, v):
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Mission must have between 1 and 3 targets')
        return v


class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int] = None
    is_completed: bool
    targets: List[TargetResponse]
    cat: Optional[CatResponse] = None

    model_config = {"from_attributes": True}
