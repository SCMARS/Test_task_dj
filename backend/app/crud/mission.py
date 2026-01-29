from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import Mission, Target
from app.schemas import MissionCreate, TargetUpdate


def create_mission(db: Session, mission_data: MissionCreate) -> Mission:
    """Create a new mission with targets."""
    mission = Mission(is_completed=False)
    db.add(mission)
    db.flush()  # Get mission ID before creating targets
    
    for target_data in mission_data.targets:
        target = Target(
            mission_id=mission.id,
            name=target_data.name,
            country=target_data.country,
            notes="",
            is_completed=False
        )
        db.add(target)
    
    db.commit()
    db.refresh(mission)
    return mission


def get_mission(db: Session, mission_id: int) -> Optional[Mission]:
    """Get a mission by ID with targets."""
    return db.query(Mission).filter(Mission.id == mission_id).first()


def get_missions(db: Session, skip: int = 0, limit: int = 100) -> List[Mission]:
    """Get all missions with pagination."""
    return db.query(Mission).offset(skip).limit(limit).all()


def delete_mission(db: Session, mission: Mission) -> None:
    """Delete a mission (targets cascade)."""
    db.delete(mission)
    db.commit()


def assign_cat_to_mission(db: Session, mission: Mission, cat_id: int) -> Mission:
    """Assign a cat to a mission."""
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission


def update_target(db: Session, target: Target, update_data: TargetUpdate) -> Target:
    """Update target notes and/or completion status."""
    if update_data.notes is not None:
        target.notes = update_data.notes
    if update_data.is_completed is not None:
        target.is_completed = update_data.is_completed
    
    db.commit()
    db.refresh(target)
    return target
