import os
import httpx
from typing import Set
from app.core.config import settings

class BreedValidator:
    """Validates cat breeds against TheCatAPI with caching."""
    
    _breeds_cache: Set[str] | None = None
    
    @classmethod
    async def get_valid_breeds(cls) -> Set[str]:
        if cls._breeds_cache is not None:
            return cls._breeds_cache
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(settings.cat_api_url, timeout=10)
                response.raise_for_status()
                breeds_data = response.json()
                cls._breeds_cache = {breed["name"] for breed in breeds_data}
                return cls._breeds_cache
        except httpx.HTTPError as e:
            raise RuntimeError(f"Failed to fetch breeds from TheCatAPI: {e}")
    
    @classmethod
    async def is_valid_breed(cls, breed_name: str) -> bool:
        """Check if breed name exists in TheCatAPI."""
        valid_breeds = await cls.get_valid_breeds()
        return breed_name in valid_breeds
    
    @classmethod
    async def validate_breed(cls, breed_name: str) -> None:
        """Validate breed and raise ValueError if invalid."""
        if not await cls.is_valid_breed(breed_name):
            # We don't fetch all breeds again for the error message to avoid spamming 
            # if cache was just populated.
            raise ValueError(
                f"Invalid breed: '{breed_name}'. "
                f"Must be one of the valid breeds from TheCatAPI."
            )
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear the breeds cache (useful for testing)."""
        cls._breeds_cache = None
