"""
Router for the API.
"""
from src import crud, models
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, APIRouter, Request, status


from config.database import get_session, engine
from datetime import datetime
from src.schema import AuthDetails
from auth import AuthHandler

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
auth_handler = AuthHandler()


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
def get_user(
    request: Request,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Get user by ID.
    """
    return crud.get_profile(db, user_id=user_id)


@router.get("/api/user/visits", tags=["User"])
def ger_user_visits(
    request: Request,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Get user visits by ID.

    """
    return crud.get_user_visits(db, user_id=user_id)


@router.post("/api/visit/", tags=["Visit"])
def create_visit(
    request: Request,
    name: str,
    date: datetime,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Create a visit.
    """
    return crud.create_visit(session=db, name=name, date=date, user_id=user_id)


@router.post("/api/user/update-password", tags=["User"], status_code=201)
def update_password(auth_details: AuthDetails, db: Session = Depends(get_session)):
    """
    Update user password.
    """
    return crud.update_password(db, auth_details=auth_details)


@router.get("/api/refresh", status_code=status.HTTP_200_OK, tags=["Token"])
def get_new_access_token(token: str):
    refesh_data = auth_handler.verify_refresh_token(token)
    new_access_token = auth_handler.create_access_token(refesh_data)
    return {
        "access_token": new_access_token,
        "token_type": "Bearer",
        "status": status.HTTP_200_OK,
    }
