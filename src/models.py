"""
Models 
"""

from datetime import datetime
from uuid import uuid4
from enum import Enum

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ENUM,CHAR
from fastapi_utils.guid_type import GUID
from config.database import Base

from auth import AuthHandler




auth_handler = AuthHandler()


class VisitState(Enum):
    """
    Enumeration of visit states.
    """
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class User(Base):
    """
    User model representing a user in the system.
    """
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True, unique=True, default=None)
    is_active = Column(Boolean, default=True)
    resident = relationship(
        "Resident",
        back_populates="user",
    )
    guard = relationship(
        "Guard",
        back_populates="user",
    )

    def __str__(self):
        return self.username

    def verify_password(self, password):
        """
        Verify the user's password.

        Args:
            password (str): Password to verify.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        auth_handler.verify_password(password, self.password)


class Visit(Base):
    """
    Visit model representing a visit record.
    """
    __tablename__ = "visit"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    date = Column(DateTime, nullable=False)
    state = Column(ENUM(VisitState), nullable=False, default=VisitState.PENDING)
    additional_info = Column(JSON, nullable=True)
    qr_id = Column(GUID, ForeignKey("qr.id"))
    visitor_id = Column(GUID, ForeignKey("visitor.id"))
    guard_id = Column(GUID, ForeignKey("guard.id"))
    resident_id = Column(GUID, ForeignKey("resident.id"))
    qr = relationship("Qr", foreign_keys=[qr_id])
    visitor = relationship("Visitor", foreign_keys=[visitor_id])
    guard = relationship("Guard", foreign_keys=[guard_id])
    resident = relationship("Resident", foreign_keys=[resident_id])


class Visitor(Base):
    """
    Visitor model representing a visitor in the system.
    """
    __tablename__ = "visitor"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    def __str__(self):
        return self.name


class FrequentVisitor(Base):
    """
    FrequentVisitor model representing a frequent visitor.
    """
    __tablename__ = "frequent_visitor"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, ForeignKey("resident.id"), primary_key=True)
    visitor_id = Column(GUID, ForeignKey("visitor.id"))


class Residence(Base):
    """
    Residence model representing a residence.
    """
    __tablename__ = "residence"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    information = Column(JSON, nullable=True)
    residents = relationship("Resident", back_populates="residence")  # add this line

    def __str__(self):
        return self.address


class Guard(Base):
    """
    Guard model representing a guard.
    """
    __tablename__ = "guard"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    user_id = Column(GUID, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id], back_populates="guard")

    def __str__(self):
        return f"{self.user.username}"


class Resident(Base):
    """
    Resident model representing a resident.
    """
    __tablename__ = "resident"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    phone = Column(String, nullable=False)
    user_id = Column(GUID, ForeignKey("user.id"))
    user = relationship("User", foreign_keys=[user_id], back_populates="resident")
    residence_id = Column(GUID, ForeignKey("residence.id"))
    residence = relationship("Residence", back_populates="resident")  # match this with Residence

    def __str__(self):
        return f"{self.user}"


class Qr(Base):
    """
    Qr model representing a QR code.
    """
    __tablename__ = "qr"
    __table_args__ = {"extend_existing": True}
    id = Column(GUID, primary_key=True, default=uuid4)
    created_date = Column(DateTime, default=datetime.now)
    code = Column(String, default=str(uuid4()))

    def __str__(self):
        return self.code
