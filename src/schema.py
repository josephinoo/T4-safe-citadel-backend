from typing import Optional, Union
from pydantic import BaseModel, UUID4
from datetime import datetime
from enum import Enum
import uuid


class AuthDetails(BaseModel):
    username: str
    password: str


class VisitState(str, Enum):
    PENDING = "PENDING"
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class UserBase(BaseModel):
    name: str
    role: str
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class VisitBase(BaseModel):
    date: Union[datetime, None] = None
    state: str = VisitState.PENDING
    visitor_id: Union[UUID4, None] = None
    guard_id: Union[UUID4, None] = None
    additional_info: Union[dict, None] = None
    qr_id: Union[UUID4, None] = None
    resident_id: Union[UUID4, None] = None


class VisitCreate(VisitBase):
    pass


class Visit(VisitBase):
    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class VisitorBase(BaseModel):
    name: str


class VisitorCreate(VisitorBase):
    pass


class Visitor(VisitorBase):
    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()
    updated_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class FrequentVisitorBase(BaseModel):
    visitor_id: UUID4


class FrequentVisitorCreate(FrequentVisitorBase):
    pass


class FrequentVisitor(FrequentVisitorBase):
    id: UUID4 = uuid.uuid4()

    class Config:
        orm_mode = True


class GuardBase(BaseModel):
    user_id: UUID4


class GuardCreate(GuardBase):
    pass


class Guard(GuardBase):
    id: UUID4 = uuid.uuid4()

    class Config:
        orm_mode = True


class ResidenceBase(BaseModel):
    address: str
    information: Optional[dict] = None
    resident_id: UUID4


class ResidenceCreate(ResidenceBase):
    pass


class Residence(ResidenceBase):
    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class ResidentBase(UserBase):
    phone: str
    user_id: Optional[UUID4] = None


class ResidentCreate(ResidentBase):
    pass


class Resident(ResidentBase):
    id: UUID4 = uuid.uuid4()

    class Config:
        orm_mode = True


class QrBase(BaseModel):
    code: str = str(uuid.uuid4())


class Qr(QrBase):
    id: UUID4 = uuid.uuid4()
    created_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class QrCreate(Qr):
    pass
