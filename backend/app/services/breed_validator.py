import os
import requests
from functools import lru_cache
from typing import Set


class BreedValidator:
    """Validates cat breeds against TheCatAPI with caching."""
    
    CAT_API_URL = os.getenv("CAT_API_URL", "https://api.thecatapi.com/v1/breeds")
    _breeds_cache: Set[str] | None = None
    
    @classmethod
    def get_valid_breeds(cls) -> Set[str]:
        """Fetch and cache valid breed names from TheCatAPI."""
        if cls._breeds_cache is not None:
            return cls._breeds_cache
        
        try:
            response = requests.get(cls.CAT_API_URL, timeout=10)
            response.raise_for_status()
            breeds_data = response.json()
            cls._breeds_cache = {breed["name"] for breed in breeds_data}
            return cls._breeds_cache
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to fetch breeds from TheCatAPI: {e}")
    
    @classmethod
    def is_valid_breed(cls, breed_name: str) -> bool:
        """Check if breed name exists in TheCatAPI."""
        valid_breeds = cls.get_valid_breeds()
        return breed_name in valid_breeds
    
    @classmethod
    def validate_breed(cls, breed_name: str) -> None:
        """Validate breed and raise ValueError if invalid."""
        if not cls.is_valid_breed(breed_name):
            valid_breeds = cls.get_valid_breeds()
            raise ValueError(
                f"Invalid breed: '{breed_name}'. "
                f"Must be one of the valid breeds from TheCatAPI."
            )
    
    @classmethod
    def clear_cache(cls) -> None:
        """Clear the breeds cache (useful for testing)."""
        cls._breeds_cache = None
