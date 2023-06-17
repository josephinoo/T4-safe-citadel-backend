"""
Database Configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://sfe:sfe@localhost/safe_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Create a new database session.

    Yields:
        Session: SQLAlchemy database session.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
