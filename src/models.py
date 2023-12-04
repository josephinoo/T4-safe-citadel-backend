from datetime import datetime
from enum import Enum
from numbers import Integral
from uuid import uuid4

from fastapi import Request
from sqlalchemy import JSON, Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.event import listens_for
from sqlalchemy.orm import class_mapper, relationship

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
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    resident_id = Column(
        UUID(as_uuid=True), ForeignKey("resident.id", ondelete="CASCADE")
    )
    guard_id = Column(UUID(as_uuid=True), ForeignKey("guard.id", ondelete="CASCADE"))
    resident = relationship(
        "Resident",
        back_populates="user",
        uselist=False,
        foreign_keys=[resident_id],
        cascade="all, delete",
    )
    guard = relationship(
        "Guard",
        back_populates="user",
        uselist=False,
        foreign_keys=[guard_id],
        cascade="all, delete",
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, role={self.role})"

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"

    def verify_password(self, password):
        return auth_handler.verify_password(password, self.password)


class Visit(Base):
    __tablename__ = "visit"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    date = Column(DateTime, nullable=False)
    register_date = Column(DateTime, default=None)
    state = Column(ENUM(VisitState), nullable=False, default=VisitState.PENDING)
    additional_info = Column(JSON, nullable=True)
    qr_id = Column(UUID(as_uuid=True), ForeignKey("qr.id", ondelete="CASCADE"))
    visitor_id = Column(
        UUID(as_uuid=True), ForeignKey("visitor.id", ondelete="CASCADE")
    )
    guard_id = Column(UUID(as_uuid=True), ForeignKey("guard.id", ondelete="CASCADE"))
    resident_id = Column(
        UUID(as_uuid=True), ForeignKey("resident.id", ondelete="CASCADE")
    )
    qr = relationship("Qr", back_populates="visit")
    visitor = relationship("Visitor", back_populates="visits")
    guard = relationship("Guard", back_populates="visits")
    resident = relationship("Resident", back_populates="visits")

    def __repr__(self):
        return f"Visit(id={self.id}, state={self.state}, date={self.date})"

    def to_dict(self):
        # Get the list of column properties
        column_props = class_mapper(self.__class__).column_attrs

        # Initialize an empty dictionary to store the attributes
        visit_dict = {}

        # Iterate through the column properties and add them to the dictionary
        for prop in column_props:
            prop_name = prop.key
            prop_value = getattr(self, prop_name)
            visit_dict[prop_name] = prop_value

        return visit_dict

    async def __admin_repr__(self, request: Request):
        return f"{self.state} - {self.date}"


class Visitor(Base):
    __tablename__ = "visitor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    visits = relationship("Visit", back_populates="visitor")

    def __repr__(self):
        return f"Visitor(id={self.id}, name={self.name})"

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"


class Residence(Base):
    __tablename__ = "residence"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    information = Column(JSON, nullable=True)
    residents = relationship(
        "Resident", secondary=residents_residences, back_populates="residences"
    )

    def __repr__(self):
        return f"Residence(id={self.id}, address={self.address})"

    async def __admin_repr__(self, request: Request):
        return f"{self.address}"


class Guard(Base):
    __tablename__ = "guard"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user = relationship(
        "User", back_populates="guard", uselist=False, passive_deletes=True
    )
    visits = relationship("Visit", back_populates="guard")

    def __repr__(self):
        return f"Guard(id={self.id})"

    async def __admin_repr__(self, request: Request):
        return f"{self.user.name}"


class Resident(Base):
    __tablename__ = "resident"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    phone = Column(String, nullable=False)
    user = relationship(
        "User", back_populates="resident", uselist=False, passive_deletes=True
    )
    residences = relationship(
        "Residence", secondary=residents_residences, back_populates="residents"
    )
    visits = relationship("Visit", back_populates="resident")

    def __repr__(self):
        return f"Resident(id={self.id}, phone={self.phone})"

    async def __admin_repr__(self, request: Request):
        return f"{self.user.name}"


class Qr(Base):
    __tablename__ = "qr"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    code = Column(String, default=str(uuid4()))
    visit = relationship("Visit", back_populates="qr", uselist=False)

    def __repr__(self):
        return f"Qr(id={self.id}, code={self.code})"


# Ensure that the User model has a relationship to the RefreshToken
    
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

