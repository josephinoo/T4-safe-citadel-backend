from sqladmin import ModelView
from src.models import User, Visit, Visitor, Resident, Residence, Qr, Guard
from typing import List


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.username, User.role]


class VisitAdmin(ModelView, model=Visit):
    column_list = [
        Visit.id,
        Visit.date,
        Visit.state,
        Visit.visitor_id,
        Visit.guard_id,
        Visit.additional_info,
        Visit.qr_id,
        Visit.resident_id,
    ]


class VisitorAdmin(ModelView, model=Visitor):
    column_list = [Visitor.id, Visitor.name]


class ResidenceAdmin(ModelView, model=Residence):
    column_list = [
        Residence.id,
        Residence.address,
        Residence.information,
    ]


class ResidentAdmin(ModelView, model=Resident):
    column_list = [Resident.id, Resident.user, Resident.user_id]


class QrAdmin(ModelView, model=Qr):
    column_list = [Qr.id]


class GuardAdmin(ModelView, model=Guard):
    column_list = [Guard.id]


admin_views = [
    UserAdmin,
    VisitAdmin,
    VisitorAdmin,
    ResidenceAdmin,
    ResidentAdmin,
    QrAdmin,
    GuardAdmin,
]
