from datetime import datetime

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from . import crud, models, utils
from .auth import AuthHandler
from .config.database import engine, get_session
from .schema import AuthDetails

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/api",
)
auth_handler = AuthHandler()


@router.post("/login/", tags=["Authorization"])
def login_user(auth_details: AuthDetails, db: Session = Depends(get_session)):
    return crud.login(db, auth_details)


@router.get("/visit/states", tags=["Visit States"])
def get_visit_states(request: Request):
    """
    Get all visit states.
    """
    return crud.get_visit_states()


@router.get("/user", tags=["User"])
def get_user(
    request: Request,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Get user by ID.
    """
    return crud.get_profile(db, user_id=user_id)


@router.get("/user/visit", tags=["User"])
def ger_user_visits(
    request: Request,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Get user visits by ID.

    """
    return crud.get_user_visits(db, user_id=user_id)


@router.post("/visit/", tags=["Visit"])
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


@router.get("/visit/{visit_id}", tags=["Visit"])
def get_visit(
    request: Request,
    visit_id: str,
    db: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Get visit by ID.
    """
    return crud.get_visit(session=db, visit_id=visit_id, user_id=user_id)


@router.post("/user/update-password", tags=["User"], status_code=201)
def update_password(auth_details: AuthDetails, db: Session = Depends(get_session)):
    """
    Update user password.
    """
    return crud.update_password(db, auth_details=auth_details)


@router.get("/refresh", status_code=status.HTTP_200_OK, tags=["Authorization"])
def get_new_access_token(token: str):
    refesh_data = auth_handler.verify_refresh_token(token)
    new_access_token = auth_handler.create_access_token(refesh_data)
    return {
        "access_token": new_access_token,
        "token_type": "Bearer",
        "status": status.HTTP_200_OK,
    }


@router.get("/qr/{qr_id}", tags=["QR Code"])
def verify_qr_code(
    request: Request,
    qr_id: str,
    session: Session = Depends(get_session),
    user_id=Depends(auth_handler.auth_wrapper),
):
    """
    Verify QR code.
    """
    return utils.verify_qr_code(session=session, qr_id=qr_id, user_id=user_id)


@router.get("/health", tags=["Health"])
def health_check(request: Request):
    """
    Health check.
    """
    if request.headers.get("X-Appengine-Cron") is None:
        return {"status": "ERROR"}
    return {"status": "OK"}
