# """
# Router for the API.
# """
# from src import crud, models, schema
# from sqlalchemy.orm import Session
# from fastapi import FastAPI, Depends, HTTPException, APIRouter
# from src import models, schema
# from config.database import SessionLocal, engine, get_db
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import datetime

# models.Base.metadata.create_all(bind=engine)

# app_router = APIRouter()


# @app_router.get("/")
# def root():
#     """
#     Root endpoint for the API.
#     """
#     return {"message": "Safe Citadel API"}


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
