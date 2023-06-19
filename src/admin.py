"""
Admin views for the models.
"""
from sqladmin import ModelView
from src.models import User, Visit, Visitor, Resident, Residence, Qr, Guard
from sqladmin import Admin


class UserAdmin(ModelView, model=User):
    """
    Admin view for the User model.
    """

    column_list = [User.id, User.name, User.username, User.role]
    icon = "fas fa-user"


class VisitAdmin(ModelView, model=Visit):
    """
    Admin view for the Visit model.
    """

    column_list = [
        Visit.id,
        Visit.date,
        Visit.state,
        Visit.visitor,
        Visit.resident_id,
    ]
    icon = "fas fa-user-friends"


class VisitorAdmin(ModelView, model=Visitor):
    """
    Admin view for the Visitor model.
    """

    column_list = [Visitor.id, Visitor.name]
    icon = "fas fa-user-friends"


class ResidenceAdmin(ModelView, model=Residence):
    """
    Admin view for the Residence model.
    """

    column_list = [
        Residence.id,
        Residence.address,
        Residence.information,
    ]
    icon = "fas fa-home"


class ResidentAdmin(ModelView, model=Resident):
    """
    Admin view for the Resident model.
    """

    column_list = [Resident.id, Resident.user, Resident.user_id]
    icon = "fas fa-user"


class QrAdmin(ModelView, model=Qr):
    """
    Admin view for the Qr model.
    """

    column_list = [Qr.id]
    icon = "fas fa-qrcode"


class GuardAdmin(ModelView, model=Guard):
    """
    Admin view for the Guard model.
    """

    column_list = [Guard.id]
    icon = "fas fa-user-shield"


admin_views = [
    UserAdmin,
    VisitAdmin,
    VisitorAdmin,
    ResidenceAdmin,
    ResidentAdmin,
    QrAdmin,
    GuardAdmin,
]


def add_views_to_app(app, engine):
    """
    Adds the admin views to the app.
    """
    admin = Admin(app, engine=engine)
    for view in admin_views:
        admin.add_view(view)
