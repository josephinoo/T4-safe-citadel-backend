from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ENUM, UUID
from config.database import Base

from auth import AuthHandler

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
    resident = relationship("Resident", back_populates="user", uselist=False)
    guard = relationship("Guard", back_populates="user", uselist=False)

    def __str__(self):
        return self.username

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


class Visitor(Base):
    __tablename__ = "visitor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visits = relationship("Visit", back_populates="visitor")

    def __str__(self):
        return self.name


class FrequentVisitor(Base):
    __tablename__ = "frequent_visitor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resident_id = Column(UUID(as_uuid=True), ForeignKey("resident.id"))
    visitor_id = Column(UUID(as_uuid=True), ForeignKey("visitor.id"))


class Residence(Base):
    __tablename__ = "residence"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    information = Column(JSON, nullable=True)
    resident_id = Column(UUID(as_uuid=True), ForeignKey("resident.id"))
    resident = relationship("Resident", back_populates="residence")

    def __str__(self):
        return self.address


class Guard(Base):
    __tablename__ = "guard"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="guard")
    visits = relationship("Visit", back_populates="guard")

    def __str__(self):
        return f"{self.user.name}"


class Resident(Base):
    __tablename__ = "resident"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    phone = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="resident")
    residence = relationship("Residence", back_populates="resident")
    visits = relationship("Visit", back_populates="resident")

    def __str__(self):
        return f"{self.user.name}"


class Qr(Base):
    __tablename__ = "qr"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.utcnow)
    code = Column(String, default=str(uuid4()))
    visit = relationship("Visit", back_populates="qr", uselist=False)

    def __str__(self):
        return self.code
