from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import Mission, Target, Cat
from app.schemas import TargetUpdate


class MissionService:
    """Business logic for mission operations."""
    
    @staticmethod
    def validate_can_assign_cat(db: Session, mission_id: int, cat_id: int) -> tuple[Mission, Cat]:
        """Validate that a cat can be assigned to a mission."""
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id {mission_id} not found"
            )
        
        if mission.is_completed:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot assign cat to completed mission"
            )
        
        if mission.cat_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Mission already has a cat assigned"
            )
        
        cat = db.query(Cat).filter(Cat.id == cat_id).first()
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id {cat_id} not found"
            )
        
        # Check if cat already has a mission
        existing_mission = db.query(Mission).filter(Mission.cat_id == cat_id).first()
        if existing_mission:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cat already assigned to mission {existing_mission.id}"
            )
        
        return mission, cat
    
    @staticmethod
    def validate_can_delete_mission(db: Session, mission_id: int) -> Mission:
        """Validate that a mission can be deleted."""
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id {mission_id} not found"
            )
        
        if mission.cat_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete mission that is assigned to a cat"
            )
        
        return mission
    
    @staticmethod
    def validate_can_update_target(
        db: Session, 
        mission_id: int, 
        target_id: int, 
        update_data: TargetUpdate
    ) -> Target:
        """Validate that target notes/completion can be updated."""
        mission = db.query(Mission).filter(Mission.id == mission_id).first()
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id {mission_id} not found"
            )
        
        target = db.query(Target).filter(
            Target.id == target_id, 
            Target.mission_id == mission_id
        ).first()
        if not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Target with id {target_id} not found in mission {mission_id}"
            )
        
        # Check if notes can be updated
        if update_data.notes is not None:
            if target.is_completed:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot update notes: target is already completed"
                )
            if mission.is_completed:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot update notes: mission is already completed"
                )
        
        return target
    
    @staticmethod
    def check_mission_completion(db: Session, mission: Mission) -> bool:
        """Check if all targets are completed and auto-complete mission if so."""
        all_completed = all(target.is_completed for target in mission.targets)
        
        if all_completed and not mission.is_completed:
            mission.is_completed = True
            db.commit()
            return True
        
        return False
