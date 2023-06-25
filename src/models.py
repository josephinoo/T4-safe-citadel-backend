from datetime import datetime
from enum import Enum
from uuid import uuid4

from fastapi import Request
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.event import listens_for
from sqlalchemy.orm import relationship

from .auth import AuthHandler
from .config.database import Base

auth_handler = AuthHandler()


class VisitState(Enum):
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Role(Enum):
    RESIDENT = "RESIDENT"
    GUARD = "GUARD"
    ADMIN = "ADMIN"


residents_residences = Table(
    "residents_residences",
    Base.metadata,
    Column("resident_id", UUID(as_uuid=True), ForeignKey("resident.id")),
    Column("residence_id", UUID(as_uuid=True), ForeignKey("residence.id")),
)


class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    role = Column(ENUM(Role), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    resident_id = Column(UUID(as_uuid=True), ForeignKey("resident.id"))
    guard_id = Column(UUID(as_uuid=True), ForeignKey("guard.id"))
    resident = relationship(
        "Resident", back_populates="user", uselist=False, foreign_keys=[resident_id]
    )
    guard = relationship(
        "Guard", back_populates="user", uselist=False, foreign_keys=[guard_id]
    )

    def __str__(self):
        return self.name

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"

    def verify_password(self, password):
        return auth_handler.verify_password(password, self.password)


class Visit(Base):
    __tablename__ = "visit"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.utcnow)
    date = Column(DateTime, nullable=False)
    state = Column(ENUM(VisitState), nullable=False, default=VisitState.PENDING)
    additional_info = Column(JSON, nullable=True)
    qr_id = Column(UUID(as_uuid=True), ForeignKey("qr.id"))
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitor.id"))
    guard_id = Column(UUID(as_uuid=True), ForeignKey("guard.id"))
    resident_id = Column(UUID(as_uuid=True), ForeignKey("resident.id"))
    qr = relationship("Qr", back_populates="visit")
    visitor = relationship("Visitor", back_populates="visits")
    guard = relationship("Guard", back_populates="visits")
    resident = relationship("Resident", back_populates="visits")

    async def __admin_repr__(self, request: Request):
        return f"{self.state} - {self.date}"

    def get(self, key):
        return self.__dict__.get(key)


class Visitor(Base):
    __tablename__ = "visitor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visits = relationship("Visit", back_populates="visitor")

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"


class Residence(Base):
    __tablename__ = "residence"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    information = Column(JSON, nullable=True)
    residents = relationship(
        "Resident",
        secondary=residents_residences,
        back_populates="residences",
    )

    async def __admin_repr__(self, request: Request):
        return f"{self.address}"


class Guard(Base):
    __tablename__ = "guard"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user = relationship("User", back_populates="guard")
    visits = relationship("Visit", back_populates="guard")

    async def __admin_repr__(self, request: Request):
        return f"{self.id}"


class Resident(Base):
    __tablename__ = "resident"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    phone = Column(String, nullable=False)
    user = relationship("User", back_populates="resident")
    residences = relationship(
        "Residence",
        secondary=residents_residences,
        back_populates="residents",
    )
    visits = relationship("Visit", back_populates="resident")

    async def __admin_repr__(self, request: Request):
        return f"{self.id}"

    def __str__(self):
        return f"{self.user}"


class Qr(Base):
    __tablename__ = "qr"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.utcnow)
    code = Column(String, default=str(uuid4()))
    visit = relationship("Visit", back_populates="qr", uselist=False)

    def __str__(self):
        return self.code


@listens_for(User, "before_delete")
def delete_related_guard_or_resident(mapper, connection, target):
    if target.guard:
        connection.execute(
            User.__table__.update()
            .where(User.guard_id == target.guard.id)
            .values(guard_id=None)
        )
        connection.execute(Guard.__table__.delete().where(Guard.id == target.guard.id))

    if target.resident:
        connection.execute(
            User.__table__.update()
            .where(User.resident_id == target.resident.id)
            .values(resident_id=None)
        )
        connection.execute(
            Resident.__table__.delete().where(Resident.id == target.resident.id)
        )
