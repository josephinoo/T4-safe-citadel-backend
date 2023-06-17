"""
Admin views for the models.
"""
from sqladmin import ModelView
from src.models import User, Visit, Visitor, Resident, Residence, Qr, Guard



class UserAdmin(ModelView, model=User):
    """
    Admin view for the User model.
    """

    column_list = [User.id, User.name, User.username, User.role]


class VisitAdmin(ModelView, model=Visit):
    """
    Admin view for the Visit model.
    """

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
    """
    Admin view for the Visitor model.
    """

    column_list = [Visitor.id, Visitor.name]


class ResidenceAdmin(ModelView, model=Residence):
    """
    Admin view for the Residence model.
    """

    column_list = [
        Residence.id,
        Residence.address,
        Residence.information,
    ]


class ResidentAdmin(ModelView, model=Resident):
    """
    Admin view for the Resident model.
    """

    column_list = [Resident.id, Resident.user, Resident.user_id]


class QrAdmin(ModelView, model=Qr):
    """
    Admin view for the Qr model.
    """

    column_list = [Qr.id]


class GuardAdmin(ModelView, model=Guard):
    """
    Admin view for the Guard model.
    """

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
