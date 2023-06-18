"""
Main module for the FastAPI application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.database import engine
from src.admin import add_views_to_app
from src.router import router

engine_db = engine

app = FastAPI()
add_views_to_app(app, engine_db)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


app.include_router(router)
