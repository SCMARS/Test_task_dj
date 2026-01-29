from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models import Cat
from app.schemas import CatCreate, CatUpdate


async def create_cat(db: AsyncSession, cat_data: CatCreate) -> Cat:
    """Create a new cat."""
    cat = Cat(
        name=cat_data.name,
        years_of_experience=cat_data.years_of_experience,
        breed=cat_data.breed,
        salary=cat_data.salary
    )
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


async def get_cat(db: AsyncSession, cat_id: int) -> Optional[Cat]:
    """Get a cat by ID."""
    result = await db.execute(select(Cat).filter(Cat.id == cat_id))
    return result.scalars().first()


async def get_cats(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Cat]:
    """Get all cats with pagination."""
    result = await db.execute(select(Cat).offset(skip).limit(limit))
    return list(result.scalars().all())


async def update_cat(db: AsyncSession, cat: Cat, cat_update: CatUpdate) -> Cat:
    """Update cat salary."""
    cat.salary = cat_update.salary
    await db.commit()
    await db.refresh(cat)
    return cat


async def delete_cat(db: AsyncSession, cat: Cat) -> None:
    """Delete a cat."""
    await db.delete(cat)
    await db.commit()
