"""
Database Configuration
"""

import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

HOSTNAME = os.environ["HOSTNAME"]
PORT = os.environ["PORT"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_USER = os.environ["DATABASE_USER"]
DATABAS_PASSWORD = os.environ["DATABASE_PASSWORD"]

DATABASE_URL = (
    f"postgresql://{DATABASE_USER}:{DATABAS_PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE_NAME}"
)
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
