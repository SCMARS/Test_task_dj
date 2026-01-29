from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models import Mission, Target, Cat
from app.schemas import TargetUpdate


class MissionService:
    """Business logic for mission operations."""
    
    @staticmethod
    async def validate_can_assign_cat(db: AsyncSession, mission_id: int, cat_id: int) -> tuple[Mission, Cat]:
        """Validate that a cat can be assigned to a mission."""
        result = await db.execute(select(Mission).filter(Mission.id == mission_id))
        mission = result.scalars().first()
        
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
        
        result_cat = await db.execute(select(Cat).filter(Cat.id == cat_id))
        cat = result_cat.scalars().first()
        
        if not cat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cat with id {cat_id} not found"
            )
        
        # Check if cat already has a mission
        result_existing = await db.execute(select(Mission).filter(Mission.cat_id == cat_id))
        existing_mission = result_existing.scalars().first()
        
        if existing_mission:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cat already assigned to mission {existing_mission.id}"
            )
        
        return mission, cat
    
    @staticmethod
    async def validate_can_delete_mission(db: AsyncSession, mission_id: int) -> Mission:
        """Validate that a mission can be deleted."""
        result = await db.execute(select(Mission).filter(Mission.id == mission_id))
        mission = result.scalars().first()
        
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
    async def validate_can_update_target(
        db: AsyncSession, 
        mission_id: int, 
        target_id: int, 
        update_data: TargetUpdate
    ) -> Target:
        result = await db.execute(select(Mission).filter(Mission.id == mission_id))
        mission = result.scalars().first()
        
        if not mission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Mission with id {mission_id} not found"
            )
        
        result_target = await db.execute(
            select(Target).filter(
                Target.id == target_id, 
                Target.mission_id == mission_id
            )
        )
        target = result_target.scalars().first()
        
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
    async def check_mission_completion(db: AsyncSession, mission: Mission) -> bool:
        
        result = await db.execute(
            select(Mission)
            .options(selectinload(Mission.targets))
            .filter(Mission.id == mission.id)
        )
        loaded_mission = result.scalars().first()
        
        all_completed = all(target.is_completed for target in loaded_mission.targets)
        
        if all_completed and not loaded_mission.is_completed:
            loaded_mission.is_completed = True
            await db.commit()
            return True
        
        return False
