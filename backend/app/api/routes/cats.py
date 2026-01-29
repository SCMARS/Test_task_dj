from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import CatCreate, CatUpdate, CatResponse
from app.crud import create_cat, get_cat, get_cats, update_cat, delete_cat
from app.services import BreedValidator

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
def create_cat_endpoint(cat_data: CatCreate, db: Session = Depends(get_db)):
    """Create a new spy cat. Breed is validated against TheCatAPI."""
    try:
        BreedValidator.validate_breed(cat_data.breed)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    
    return create_cat(db, cat_data)


@router.get("/", response_model=List[CatResponse])
def list_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all spy cats with pagination."""
    return get_cats(db, skip=skip, limit=limit)


@router.get("/{cat_id}", response_model=CatResponse)
def get_cat_endpoint(cat_id: int, db: Session = Depends(get_db)):
    """Get a single spy cat by ID."""
    cat = get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return cat


@router.patch("/{cat_id}", response_model=CatResponse)
def update_cat_endpoint(cat_id: int, cat_update: CatUpdate, db: Session = Depends(get_db)):
    """Update a spy cat's salary."""
    cat = get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return update_cat(db, cat, cat_update)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat_endpoint(cat_id: int, db: Session = Depends(get_db)):
    """Delete a spy cat from the system."""
    cat = get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    delete_cat(db, cat)
    return None
