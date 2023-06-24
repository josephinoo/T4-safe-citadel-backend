"""
Main module for the FastAPI application.
"""

import os
import sys

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.admin import add_views_to_app
from src.config.database import Base, engine, get_session
from src.router import router

# Agregar el directorio padre al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

engine_db = engine

description = """
🏰 El Safe Citadel API es una interfaz de programación de aplicaciones (API) diseñada para el control seguro de visitas a una ciudadela.
### ✨ Características:

- Gestión de reservas
- Verificación de identidad de visitantes
- Generación de códigos de acceso únicos
- Registro de eventos de accesoia
🔒 Proporciona una solución completa y confiable para el control de \n#
visitas a la ciudadela, garantizando la seguridad y el orden en el acceso
al sitio histórico.

¡Experimenta la tranquilidad de administrar y controlar las visitas a la ciudadela de
manera segura con el Safe Citadel API! 🚪🔐"""

tags_metadata = [
    {"name": "Authorization", "description": "Autenticación de usuarios"},
    {"name": "Visit States", "description": "Estados de las visitas"},
    {"name": "User", "description": "Información de usuarios"},
    {"name": "Visit", "description": "Información de visitas"},
]
app = FastAPI(
    dependencies=[Depends(get_session)],
    title="Safe Citadel API",
    version="0.1.0",
    description=description,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
)
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

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


@app.get("/healthcheck")
def healthcheck():
    """
    Healthcheck endpoint
    """
    return {"status": "ok"}


@app.get("/")
def index():
    """
    Index endpoint
    """
    return {"status": "ok"}
