import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from pydantic import UUID4, BaseModel


class AuthDetails(BaseModel):
    """
    Authentication details.
    """

    username: str
    password: str


class VisitState(str, Enum):
    """
    Enumeration of visit states.
    """

    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class UserBase(BaseModel):
    """
    Base model for User.
    """

    name: str
    role: str
    username: str


class UserCreate(UserBase):
    """
    Model for creating a User.
    """


class User(UserBase):
    """
    User model.
    """

    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class VisitBase(BaseModel):
    """
    Base model for Visit.
    """

    date: Union[datetime, None] = None
    state: str = VisitState.PENDING
    visitor_id: Union[UUID4, None] = None
    guard_id: Union[UUID4, None] = None
    additional_info: Union[dict, None] = None
    qr_id: Union[UUID4, None] = None
    resident_id: Union[UUID4, None] = None


class VisitCreate(VisitBase):
    """
    Model for creating a Visit.
    """


class Visit(VisitBase):
    """
    Visit model.
    """

    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class VisitorBase(BaseModel):
    """
    Base model for Visitor.
    """

    name: str


class VisitorCreate(VisitorBase):
    """
    Model for creating a Visitor.
    """


class Visitor(VisitorBase):
    """
    Visitor model.
    """

    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class FrequentVisitorBase(BaseModel):
    """
    Base model for FrequentVisitor.
    """

    visitor_id: UUID4


class FrequentVisitorCreate(FrequentVisitorBase):
    """
    Model for creating a FrequentVisitor.
    """


class FrequentVisitor(FrequentVisitorBase):
    """
    FrequentVisitor model.
    """

    id: UUID4 = uuid.uuid4()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class GuardBase(BaseModel):
    """
    Base model for Guard.
    """

    user_id: UUID4


class GuardCreate(GuardBase):
    """
    Model for creating a Guard.
    """


class Guard(GuardBase):
    """
    Guard model.
    """

    id: UUID4 = uuid.uuid4()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class ResidenceBase(BaseModel):
    """
    Base model for Residence.
    """

    address: str
    information: Optional[dict] = None
    resident_id: UUID4


class ResidenceCreate(ResidenceBase):
    """
    Model for creating a Residence.
    """


class Residence(ResidenceBase):
    """
    Residence model.
    """

    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class ResidentBase(UserBase):
    """
    Base model for Resident.
    """

    phone: str
    user_id: Optional[UUID4] = None


class ResidentCreate(ResidentBase):
    """
    Model for creating a Resident.
    """


class Resident(ResidentBase):
    """
    Resident model.
    """

    id: UUID4 = uuid.uuid4()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class QrBase(BaseModel):
    """
    Base model for Qr.
    """

    code: str = str(uuid.uuid4())


class Qr(QrBase):
    """
    Qr model.
    """

    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        """Pydantic configuration."""

        orm_mode = True


class QrCreate(Qr):
    """
    Model for creating a Qr.
    """


class UserLogin(BaseModel):
    """
    Model for login.
    """

    username: str
    password: str
