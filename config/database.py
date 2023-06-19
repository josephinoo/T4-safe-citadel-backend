"""
Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql://sfe:sfe@localhost/safe_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()


def get_session() -> sessionmaker:
    """
    Get a new database session.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
