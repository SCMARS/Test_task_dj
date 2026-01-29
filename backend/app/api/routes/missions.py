from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas import MissionCreate, MissionResponse, TargetUpdate, TargetResponse
from app.crud import create_mission, get_mission, get_missions, delete_mission, assign_cat_to_mission, update_target
from app.services import MissionService

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
async def create_mission_endpoint(mission_data: MissionCreate, db: AsyncSession = Depends(get_db)):
    """Create a new mission with 1-3 targets."""
    return await create_mission(db, mission_data)


@router.get("/", response_model=List[MissionResponse])
async def list_missions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all missions with their targets."""
    return await get_missions(db, skip=skip, limit=limit)


@router.get("/{mission_id}", response_model=MissionResponse)
async def get_mission_endpoint(mission_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single mission by ID with all targets."""
    mission = await get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mission_endpoint(mission_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a mission (only if not assigned to a cat)."""
    mission = await MissionService.validate_can_delete_mission(db, mission_id)
    await delete_mission(db, mission)
    return None


@router.post("/{mission_id}/assign/{cat_id}", response_model=MissionResponse)
async def assign_cat_endpoint(mission_id: int, cat_id: int, db: AsyncSession = Depends(get_db)):
    """Assign a cat to a mission."""
    mission, cat = await MissionService.validate_can_assign_cat(db, mission_id, cat_id)
    return await assign_cat_to_mission(db, mission, cat_id)


@router.patch("/{mission_id}/targets/{target_id}", response_model=TargetResponse)
async def update_target_endpoint(
    mission_id: int, 
    target_id: int, 
    update_data: TargetUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update target notes and/or completion status. Notes freeze when target/mission is completed."""
    target = await MissionService.validate_can_update_target(db, mission_id, target_id, update_data)
    updated_target = await update_target(db, target, update_data)
    
    # Check for mission auto-completion
    mission = await get_mission(db, mission_id)
    await MissionService.check_mission_completion(db, mission)
    
    return updated_target
