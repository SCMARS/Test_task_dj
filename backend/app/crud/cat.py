from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import Cat
from app.schemas import CatCreate, CatUpdate


def create_cat(db: Session, cat_data: CatCreate) -> Cat:
    """Create a new cat."""
    cat = Cat(
        name=cat_data.name,
        years_of_experience=cat_data.years_of_experience,
        breed=cat_data.breed,
        salary=cat_data.salary
    )
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


def get_cat(db: Session, cat_id: int) -> Optional[Cat]:
    """Get a cat by ID."""
    return db.query(Cat).filter(Cat.id == cat_id).first()


def get_cats(db: Session, skip: int = 0, limit: int = 100) -> List[Cat]:
    """Get all cats with pagination."""
    return db.query(Cat).offset(skip).limit(limit).all()


def update_cat(db: Session, cat: Cat, cat_update: CatUpdate) -> Cat:
    """Update cat salary."""
    cat.salary = cat_update.salary
    db.commit()
    db.refresh(cat)
    return cat


def delete_cat(db: Session, cat: Cat) -> None:
    """Delete a cat."""
    db.delete(cat)
    db.commit()
