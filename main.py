"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine
from src.admin import add_views_to_app
from src.router import router
from config.database import get_session, Base


engine_db = engine


app = FastAPI(
    dependencies=[Depends(get_session)],
    title="Safe Citadel API",
    version="0.1.0",
    description="API for Safe Citadel",
)
Base.metadata.create_all(bind=engine_db)


add_views_to_app(app, engine_db)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
