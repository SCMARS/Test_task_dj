from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.schemas import CatCreate, CatUpdate, CatResponse
from app.crud import create_cat, get_cat, get_cats, update_cat, delete_cat
from app.services import BreedValidator

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post("/", response_model=CatResponse, status_code=status.HTTP_201_CREATED)
async def create_cat_endpoint(cat_data: CatCreate, db: AsyncSession = Depends(get_db)):
    """Create a new spy cat. Breed is validated against TheCatAPI."""
    try:
        await BreedValidator.validate_breed(cat_data.breed)
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
    
    return await create_cat(db, cat_data)


@router.get("/", response_model=List[CatResponse])
async def list_cats(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all spy cats with pagination."""
    return await get_cats(db, skip=skip, limit=limit)


@router.get("/{cat_id}", response_model=CatResponse)
async def get_cat_endpoint(cat_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single spy cat by ID."""
    cat = await get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return cat


@router.patch("/{cat_id}", response_model=CatResponse)
async def update_cat_endpoint(cat_id: int, cat_update: CatUpdate, db: AsyncSession = Depends(get_db)):
    """Update a spy cat's salary."""
    cat = await get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    return await update_cat(db, cat, cat_update)


@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cat_endpoint(cat_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a spy cat from the system."""
    cat = await get_cat(db, cat_id)
    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    await delete_cat(db, cat)
    return None
