from pydantic import BaseModel, Field


class CatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    years_of_experience: int = Field(..., ge=0)
    breed: str = Field(..., min_length=1, max_length=100)
    salary: float = Field(..., gt=0)


class CatCreate(CatBase):
    pass


class CatUpdate(BaseModel):
    salary: float = Field(..., gt=0)


class CatResponse(CatBase):
    id: int

    model_config = {"from_attributes": True}
