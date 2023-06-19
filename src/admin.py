from starlette_admin.contrib.sqla import Admin, ModelView
from src.models import User, Resident, Residence, Visit, Qr, Guard, Visitor


def add_views_to_app(app, engine_db):
    admin = Admin(engine_db, title="Safe Citadel API")
    admin.add_view(ModelView(User, icon="fa fa-user", label="User"))
    admin.add_view(ModelView(Resident, icon="fa fa-user"))
    admin.add_view(ModelView(Residence, icon="fa fa-home"))
    admin.add_view(ModelView(Visit, icon="fa fa-calendar"))
    admin.add_view(ModelView(Qr, icon="fa fa-qrcode"))
    admin.add_view(ModelView(Guard, icon="fa fa-shield"))
    admin.add_view(ModelView(Visitor, icon="fa fa-user"))

    admin.mount_to(app)
