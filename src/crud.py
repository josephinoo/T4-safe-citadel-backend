"""
Crud module
"""

from typing import Type
from datetime import datetime
import uuid
import itertools
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.orm import class_mapper, defer
from fastapi import Response, status

from config.database import Base
from src import models, schema


def create_model(db: Session, model_schema: Type[BaseModel], model: Type[Base]):
    """
    Create a new model instance in the database.

    Args:
        db (Session): SQLAlchemy database session.
        model_schema (Type[BaseModel]): Pydantic model schema.
        model (Type[Base]): SQLAlchemy model.

    Returns:
        db_model: Created model instance.
    """
    db_model = model(**model_schema.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def create_visitor(db: Session, name: str):
    """
    Create a new visitor record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        name (str): Name of the visitor.

    Returns:
        Visitor: Created visitor instance.
    """
    while True:
        new_id = uuid.uuid4()
        existing_visitor = db.query(models.Visitor).filter_by(id=new_id).first()
        if existing_visitor is None:
            visitor = models.Visitor(id=new_id, name=name)
            db.add(visitor)
            db.commit()
            return visitor
        return existing_visitor


def create_qr(db: Session):
    """
    Create a new QR code record in the database.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        Qr: Created QR code instance.
    """
    while True:
        new_id = uuid.uuid4()
        existing_qr = db.query(models.Qr).filter_by(id=new_id).first()
        if existing_qr is None:
            qr = models.Qr(id=new_id)
            db.add(qr)
            db.commit()
            return qr
        return existing_qr


def create_visit(session: Session, name: str, date: datetime, user_id: uuid.UUID):
    """
    Create a new visit record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        name (str): Name of the visitor.
        date (datetime): Date of the visit.
        visit (schema.VisitCreate): Visit data.

    Returns:
        Visit: Created visit instance.
    """
    visit = schema.VisitCreate()
    resident = session.query(models.Resident).filter_by(user_id=user_id).first()
    visit.qr_id = create_qr(session).id
    visit.visitor_id = create_visitor(session, name).id
    visit.date = date
    visit.resident_id = resident.id
    visit.state = schema.VisitState.PENDING
    new_visit = create_model(session, visit, models.Visit)
    return new_visit


def create_residence(db: Session, address: str, resident_id: uuid.UUID):
    """
    Create a new residence record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        address (str): Address of the residence.
        resident_id (uuid.UUID): ID of the resident.

    Returns:
        Residence: Created residence instance.
    """
    while True:
        new_id = uuid.uuid4()
        existing_residence = db.query(models.Residence).filter_by(id=new_id).first()
        if existing_residence is None:
            residence = models.Residence(
                id=new_id, address=address, resident_id=resident_id
            )
            db.add(residence)
            db.commit()
            return residence
        return existing_residence


def create_user(db: Session, user: schema.UserCreate):
    """
    Create a new user record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        user (schema.UserCreate): User data.

    Returns:
        User: Created user instance.
    """
    while True:
        new_id = uuid.uuid4()
        existing_user = db.query(models.User).filter_by(id=new_id).first()
        if existing_user is None:
            user = models.User(id=new_id, **user.dict())
            db.add(user)
            db.commit()
            return user
        return existing_user


def create_resident(db: Session, address: str, resident: schema.ResidentCreate):
    """
    Create a new resident record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        address (str): Address of the residence.
        resident (schema.ResidentCreate): Resident data.

    Returns:
        Resident: Created resident instance.
    """
    user = schema.UserCreate(
        role="resident",
        name=resident.name,
        username=resident.username,
    )
    user = create_user(
        db,
        user=user,
    )
    user_id = user.id
    resident.user_id = user_id
    resident = create_model(db, resident, models.Resident)
    create_residence(db=db, address=address, resident_id=resident.id)
    return resident


def get_visit_states():
    """
    Get the list of visit states.

    Returns:
        dict: Visit states.
    """
    list_visits_state = [
        schema.VisitState.PENDING,
        schema.VisitState.REGISTERED,
        schema.VisitState.CANCELLED,
        schema.VisitState.EXPIRED,
    ]
    return {"visit_state": list_visits_state}


def get_profile(db: Session, user_id: uuid.UUID):
    """
    Get the profile of a user.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (uuid.UUID): ID of the user.

    Returns:
        dict: User profile.
    """
    user = db.query(models.User).filter_by(id=user_id).first()

    if user and user.role == "RESIDENT":
        resident = db.query(models.Resident).filter_by(user_id=user_id).first()
        residence = (
            db.query(models.Residence).filter_by(id=resident.residence_id).first()
        )
        return {
            "user": {
                "id": user.id,
                "name": user.name,
                "username": user.username,
                "phone": resident.phone,
            },
            "residence": {
                "address": residence.address,
                "created_at": residence.created_date,
                "information": residence.information,
            },
        }
    return {"user": user}


def defer_everything_but(entity, cols):
    m = class_mapper(entity)
    return [
        defer(k)
        for k in {
            p.key for p in m.iterate_properties if hasattr(p, "columns")
        }.difference(cols)
    ]


def get_user_visits(db: Session, user_id: uuid.UUID):
    """
    Get the visits of a user.

    Args:
        db (Session): SQLAlchemy database session.
        user_id (uuid.UUID): ID of the user.

    Returns:
        dict: User visits.
    """
    user = db.query(models.User).filter_by(id=user_id).first()

    if user and user.role == "RESIDENT":
        resident = db.query(models.Resident).filter_by(user_id=user_id).first()
        visit = db.query(models.Visit).filter_by(resident_id=resident.id).all()
        grouped = {k: list(g) for k, g in itertools.groupby(visit, lambda t: t.state)}
        return {"visits": grouped}


def login(db: Session, user: schema.UserLogin):
    """
    Login a user.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: User data.
    """
    user = (
        db.query(models.User)
        .filter_by(username=user.username, password=user.password)
        .first()
    )
    print(user)
    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    return {"user": user}
