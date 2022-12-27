from typing import MutableMapping, List, Union
from datetime import datetime
from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    
    # In search of better saving jwt secret and other approaches to secure the app
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = "HS256"
    
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    username: str = os.getenv("PGUSER")
    password: str = os.getenv("PGPASSWORD")
    database: str = os.getenv("DATABASE")
    
    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://{username}:{password}@localhost:5432/{database}"
    
    JWTPayloadMapping = MutableMapping[
        str, Union[datetime, bool, str, List[str], List[int]]
    ]


settings = Settings()
