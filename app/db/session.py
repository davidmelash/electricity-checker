import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

username = os.getenv("PGUSER")
password = os.getenv("PGPASSWORD")
database = os.getenv("DATABASE")

SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost:5432/{database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
