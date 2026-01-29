from pydantic_settings import BaseSettings
from typing import ClassVar

class Settings(BaseSettings):
    PROJECT_NAME: str = "Spy Cat Agency API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./spy_cat_agency.db"
    cat_api_url: str = "https://api.thecatapi.com/v1/breeds"
    
    model_config = {"case_sensitive": False, "env_file": ".env"}

settings = Settings()
