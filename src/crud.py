import os
import time
import uuid
from datetime import date, datetime
from typing import Type  # noqa: UP035

from fastapi import Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session, class_mapper, defer

from . import models, schema, utils
from .auth import AuthHandler
from .config.database import Base

os.environ["TZ"] = "America/Guayaquil"
time.tzset()

auth_handler = AuthHandler()


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
    user = session.query(models.User).filter_by(id=user_id).first()
    visit = schema.VisitCreate()

    if user.role == models.Role.GUARD:
        visit.state = schema.VisitState.REGISTERED
        visit.date = date
        visit.visitor_id = create_visitor(session, name).id
        new_visit = create_model(session, visit, models.Visit)
        return new_visit

    resident = session.query(models.Resident)
    resident = resident.join(models.User).filter(models.User.id == user_id).first()
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
    if user is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    if user.role == models.Role.RESIDENT:
        resident = db.query(models.Resident)
        resident = resident.join(models.User).filter(models.User.id == user_id).first()
        if resident is None:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        visits = db.query(models.Visit).filter_by(resident_id=resident.id).all()

        grouped = utils.grouped_dict(visits)
        for key in grouped.keys():
            for visit in grouped[key]:
                visitor = (
                    db.query(models.Visitor).filter_by(id=visit.visitor_id).first()
                )
                visit.visitor = visitor
        return {"visits": grouped}
    if user.role == models.Role.GUARD:
        guard = db.query(models.Guard)
        guard = guard.join(models.User).filter(models.User.id == user_id).first()
        if guard is None:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        visits = (
            db.query(models.Visit)
            .filter(models.Visit.date.between(start_of_day, end_of_day))
            .all()
        )
        gruoped_visits = utils.grouped_dict(visits)
        for key in gruoped_visits.keys():
            for visit in gruoped_visits[key]:
                visitor = (
                    db.query(models.Visitor).filter_by(id=visit.visitor_id).first()
                )
                resident = (
                    db.query(models.Resident).filter_by(id=visit.resident_id).first()
                )
                visit.visitor = visitor
                visit.resident = resident
        return {"visits": gruoped_visits}


def login(db: Session, auth_details: schema.AuthDetails):
    """
    Login a user.

    Args:
        db (Session): SQLAlchemy database session.
        username (str): Username of the user.
        password (str): Password of the user.

    Returns:
        dict: User data.
    """
    user = db.query(models.User).filter_by(username=auth_details.username).first()
    if (user is None) or (
        not auth_handler.verify_password(auth_details.password, user.password)
    ) or (not user.is_active):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    token = auth_handler.encode_token(user.id)
    refresh_token = auth_handler.refresh_token(token)
    return {
        "token": token,
        "refresh_token": refresh_token,
    }


def update_password(db: Session, auth_details: schema.AuthDetails):
    """
    Update user password
    """
    user = db.query(models.User).filter_by(username=auth_details.username).first()
    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    hash_password = auth_handler.get_password_hash(auth_details.password)
    user.password = hash_password
    db.commit()
    return {"user": user}


def get_visit(session: Session, visit_id: uuid.UUID, user_id: uuid.UUID):
    """
    Get a visit by id
    """
    user = session.query(models.User).filter_by(id=user_id).first()
    if user.role == models.Role.GUARD:
        return session.query(models.Visit).filter_by(id=visit_id).first()

    resident = session.query(models.Resident)
    resident = resident.join(models.User).filter(models.User.id == user_id).first()
    if resident is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    visit = session.query(models.Visit).filter(models.Visit.id == visit_id).first()

    if visit is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visitor = session.query(models.Visitor).filter_by(id=visit.visitor_id).first()
    return {"visit": visit, "visitor": visitor}


def register_visit(session: Session, qr_id: uuid.UUID, user_id: uuid.UUID):
    """
    Register a visit by QR code
    """
    qr = session.query(models.Qr).filter_by(id=qr_id).first()
    if qr is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visit = session.query(models.Visit).filter_by(qr_id=qr_id).first()
    if visit.state.value == schema.VisitState.REGISTERED.value:
        return Response(status_code=status.HTTP_409_CONFLICT)
    visit.state = schema.VisitState.REGISTERED
    visit.register_date = datetime.now()
    session.commit()
    return visit


def canceled_visit(session: Session, qr_id: uuid.UUID, user_id: uuid.UUID):
    """
    Cancel a visit by QR code
    """
    qr = session.query(models.Qr).filter_by(id=qr_id).first()
    if qr is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visit = session.query(models.Visit).filter_by(qr_id=qr_id).first()
    if visit.state.value == schema.VisitState.CANCELLED.value:
        return Response(status_code=status.HTTP_409_CONFLICT)
    visit.state = schema.VisitState.CANCELLED
    visit.register_date = datetime.now()
    session.commit()
    return visit


def verify_visit(session: Session, qr_id: uuid.UUID, user_id: uuid.UUID):
    """
    Verify a visit by QR code
    """
    qr = session.query(models.QR).filter_by(id=qr_id).first()
    if qr is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visit = session.query(models.Visit).filter_by(qr_id=qr_id).first()
    if (
        visit.state.value == schema.VisitState.REGISTERED.value
        or visit.state.value == schema.VisitState.CANCELLED
    ):
        return Response(status_code=status.HTTP_409_CONFLICT)
    return visit
