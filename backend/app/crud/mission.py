from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models import Mission, Target
from app.schemas import MissionCreate, TargetUpdate


async def create_mission(db: AsyncSession, mission_data: MissionCreate) -> Mission:
    """Create a new mission with targets."""
    mission = Mission(is_completed=False)
    db.add(mission)
    await db.flush()  
    
    for target_data in mission_data.targets:
        target = Target(
            mission_id=mission.id,
            name=target_data.name,
            country=target_data.country,
            notes="",
            is_completed=False
        )
        db.add(target)
    
    await db.commit()
    await db.refresh(mission)
    return mission


async def get_mission(db: AsyncSession, mission_id: int) -> Optional[Mission]:
    result = await db.execute(select(Mission).filter(Mission.id == mission_id))
    return result.scalars().first()


async def get_missions(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Mission]:
    """Get all missions with pagination."""
    result = await db.execute(select(Mission).offset(skip).limit(limit))
    return list(result.scalars().all())


async def delete_mission(db: AsyncSession, mission: Mission) -> None:
    """Delete a mission (targets cascade)."""
    await db.delete(mission)
    await db.commit()


async def assign_cat_to_mission(db: AsyncSession, mission: Mission, cat_id: int) -> Mission:
    """Assign a cat to a mission."""
    mission.cat_id = cat_id
    await db.commit()
    await db.refresh(mission)
    return mission


async def update_target(db: AsyncSession, target: Target, update_data: TargetUpdate) -> Target:
    """Update target notes and/or completion status."""
    if update_data.notes is not None:
        target.notes = update_data.notes
    if update_data.is_completed is not None:
        target.is_completed = update_data.is_completed
    
    await db.commit()
    await db.refresh(target)
    return target
