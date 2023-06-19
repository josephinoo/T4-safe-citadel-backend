"""
Router for the API.
"""
from src import crud, models, schema
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request

from src import models, schema
from config.database import get_session, engine
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from src.schema import AuthDetails

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/")
def root(request: Request):
    """
    Root endpoint for the API.
    """
    return {"message": "Safe Citadel API"}


@router.post("/api/login/", tags=["User"])
def login_user(auth_details: AuthDetails, db: Session = Depends(get_session)):
    return crud.login(db, auth_details)


@router.get("/visit/states", tags=["Visit States"])
def get_visit_states(request: Request):
    """
    Get all visit states.
    """
    return crud.get_visit_states()


@router.get("/api/user", tags=["User"])
def get_user(request: Request, db: Session = Depends(get_session)):
    """
    Get user by ID.
    """
    user_id = request.headers.get("user_id")
    return crud.get_profile(db, user_id=user_id)


@router.get("/api/user/visits", tags=["User"])
def ger_user_visits(request: Request, db: Session = Depends(get_session)):
    """
    Get user visits by ID.

    """
    user_id = request.headers.get("user_id")
    return crud.get_user_visits(db, user_id=user_id)


@router.post("/api/visit/", tags=["Visit"])
def create_visit(
    request: Request, name: str, date: datetime, db: Session = Depends(get_session)
):
    """
    Create a visit.
    """
    user_id = request.headers.get("user_id")
    return crud.create_visit(session=db, name=name, date=date, user_id=user_id)


@router.post("/api/user/update-password", tags=["User"], status_code=201)
def update_password(auth_details: AuthDetails, db: Session = Depends(get_session)):
    """
    Update user password.
    """
    return crud.update_password(db, auth_details=auth_details)
