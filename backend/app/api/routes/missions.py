from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import MissionCreate, MissionResponse, TargetUpdate, TargetResponse
from app.crud import create_mission, get_mission, get_missions, delete_mission, assign_cat_to_mission, update_target
from app.services import MissionService

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission_endpoint(mission_data: MissionCreate, db: Session = Depends(get_db)):
    """Create a new mission with 1-3 targets."""
    return create_mission(db, mission_data)


@router.get("/", response_model=List[MissionResponse])
def list_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all missions with their targets."""
    return get_missions(db, skip=skip, limit=limit)


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission_endpoint(mission_id: int, db: Session = Depends(get_db)):
    """Get a single mission by ID with all targets."""
    mission = get_mission(db, mission_id)
    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mission with id {mission_id} not found"
        )
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission_endpoint(mission_id: int, db: Session = Depends(get_db)):
    """Delete a mission (only if not assigned to a cat)."""
    mission = MissionService.validate_can_delete_mission(db, mission_id)
    delete_mission(db, mission)
    return None


@router.post("/{mission_id}/assign/{cat_id}", response_model=MissionResponse)
def assign_cat_endpoint(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    """Assign a cat to a mission."""
    mission, cat = MissionService.validate_can_assign_cat(db, mission_id, cat_id)
    return assign_cat_to_mission(db, mission, cat_id)


@router.patch("/{mission_id}/targets/{target_id}", response_model=TargetResponse)
def update_target_endpoint(
    mission_id: int, 
    target_id: int, 
    update_data: TargetUpdate,
    db: Session = Depends(get_db)
):
    """Update target notes and/or completion status. Notes freeze when target/mission is completed."""
    target = MissionService.validate_can_update_target(db, mission_id, target_id, update_data)
    updated_target = update_target(db, target, update_data)
    

    mission = get_mission(db, mission_id)
    MissionService.check_mission_completion(db, mission)
    
    return updated_target
