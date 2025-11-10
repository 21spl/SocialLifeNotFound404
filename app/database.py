from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from .models import Base

db_url = "postgresql+psycopg://user:secret@localhost:5432/SocialMediaDB"

engine = create_engine(db_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Dependency to get a database session
db = Annotated[Session, Depends(get_db)] 

# Create tables for all table models
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
