from abc import abstractmethod
from typing import Any, Dict

from fastapi import Request
from starlette_admin.contrib.sqla import Admin, ModelView

from src.auth import AuthHandler, MyAuthProvider
from src.models import Guard, Qr, Residence, Resident, User, Visit, Visitor

auth_handler = AuthHandler()


class UserView(ModelView):
    exclude_fields_from_list = [
        "id",
        "password",
        "created_date",
        "updated_date",
        "resident_id",
        "guard_id",
        "qr_id",
        "visitor_id",
        "resident",
        "guard",
    ]

    @abstractmethod
    async def create(self, request: Request, data: Dict) -> Any:
        """
        Create item
        Parameters:
            request: The request being processed
            data: Dict values contained converted form data
        Returns:
            Any: Created Item
        """
        data["password"] = auth_handler.get_password_hash(data["password"])
        return await super().create(request, data)


def add_views_to_app(app, engine_db):
    admin = Admin(
        engine_db,
        title="Safe Citadel API",
        auth_provider=MyAuthProvider(),
        base_url="/admin",
    )
    admin.add_view(UserView(User, icon="fa fa-user", label="User"))
    admin.add_view(ModelView(Resident, icon="fa fa-user"))
    admin.add_view(ModelView(Residence, icon="fa fa-home"))
    admin.add_view(ModelView(Visit, icon="fa fa-calendar"))
    admin.add_view(ModelView(Qr, icon="fa fa-qrcode"))
    admin.add_view(ModelView(Guard, icon="fa fa-shield"))
    admin.add_view(ModelView(Visitor, icon="fa fa-user"))
    admin.mount_to(app)
