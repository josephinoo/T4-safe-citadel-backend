"""
Router for the API.
"""
from src import crud, models, schema
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter,Request

from src import models, schema
from config.database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

router = APIRouter()



@router.get("/")
def root(request: Request):
    """
    Root endpoint for the API.
    """
    return {"message": "Safe Citadel API"}

@router.post("/api/login/",  tags=["User"])
async def login_user(user:schema.UserLogin, db: Session = Depends(get_db)):
    return crud.login(db, user)
   

@router.get("/visit/states", tags=["Visit States"])
def get_visit_states(request: Request):
    """
    Get all visit states.
    """
    return crud.get_visit_states()


@router.get("/api/user", tags=["User"])
def get_user(request: Request, db: Session = Depends(get_db)):
    """
    Get user by ID.
    """
    user_id = request.headers.get("user_id")
    return crud.get_profile(db, user_id=user_id)


@router.get("/api/user/visits", tags=["User"])
def ger_user_visits(request: Request, db: Session = Depends(get_db)):
    """
    Get user visits by ID.
    
    """
    user_id = request.headers.get("user_id")
    return crud.get_user_visits(db, user_id=user_id)

@router.post("/api/visit/", response_model=schema.Visit, tags=["Visit"])
def create_visit(request: Request,name:str ,date: datetime, visit: schema.VisitCreate, db: Session = Depends(get_db)):
    """
    Create a visit.
    """
    user_id = request.headers.get("user_id")
    return crud.create_visit(db=db, name=name, date=date, visit=visit, user_id=user_id)

# # User
# @app_router.post("/login", tags=["User"])
# def login(username: str, password=str, db: Session = Depends(get_db)):
#     """
#     Login endpoint for the user.

#     Args:
#         username (str): User's username.
#         password (str): User's password.
#         db (Session): SQLAlchemy database session.

#     Returns:
#         str: Placeholder return value.
#     """
#     return ""


# # # GET
# # @app_router.get("/api/user/{user_id}", response_model=schema.User, tags=["User"])
# # def get_user(user_id: str, db: Session = Depends(get_db)):
# #     db_user = crud.get_user(db, user_id=user_id)
# #     if db_user is None:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     return db_user


# # @app_router.get("/visit/states", tags=["Visit States"])
# # def get_visit_states(db: Session = Depends(get_db)):
# #     return crud.get_visit_states()


# # # POST


# # app_router.post("/api/user/", response_model=schema.User, tags=["User"])
# # def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
# #     return crud.create_user(db=db, user=user)


# # app_router.post("/api/visit/", response_model=schema.Visit, tags=["Visit"])
# # def create_visit(
# #     visit: schema.VisitCreate, name: str, date: datetime, db: Session = Depends(get_db)
# # ):
# #     return crud.create_visit(db=db, name=name, date=date, visit=visit)


# # app_router.post("/api/resident/", response_model=schema.Resident, tags=["Resident"])
# # def create_resident(
# #     resident: schema.ResidentCreate, address: str, db: Session = Depends(get_db)
# # ):
# #     return crud.create_resident(db=db, resident=resident, address=address)
