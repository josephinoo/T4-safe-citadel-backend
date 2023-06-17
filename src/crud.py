from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Type
from config.database import Base
from src import models, schema
from datetime import datetime
import uuid


def create_model(db: Session, model_schema: Type[BaseModel], model: Type[Base]):
    db_model = model(**model_schema.dict())
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


# CREATE
def create_visitor(db: Session, name: str):
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
    while True:
        new_id = uuid.uuid4()
        existing_qr = db.query(models.Qr).filter_by(id=new_id).first()
        if existing_qr is None:
            qr = models.Qr(id=new_id)
            db.add(qr)
            db.commit()
            return qr
        return existing_qr


def create_visit(db: Session, name: str, date: datetime, visit: schema.VisitCreate):
    visit.qr_id = create_qr(db).id
    visit.visitor_id = create_visitor(db, name).id
    visit.date = date
    return create_model(db, visit, models.Visit)


def create_residence(db: Session, address: str, resident_id: uuid.UUID):
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
    list_visits_state = [
        schema.VisitState.PENDING,
        schema.VisitState.REGISTERED,
        schema.VisitState.CANCELLED,
        schema.VisitState.EXPIRED,
    ]
    return {"visit_state": list_visits_state}
