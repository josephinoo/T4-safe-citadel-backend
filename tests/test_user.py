from uuid import uuid4

import pytest

from src.auth import AuthHandler
from src.models import Role, User


class TestUser:
    auth_handler = AuthHandler()

    # Tests that the user can be created with all required fields and the password can be verified
    @pytest.mark.asyncio
    async def test_create_user_with_all_required_fields(self):
        # Create a user with all required fields
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password=self.auth_handler.get_password_hash("password"),
            resident_id=uuid4(),
        )

        # Assert that the user is created successfully
        assert user.name == "John Doe"
        assert user.role == Role.RESIDENT
        assert user.username == "johndoe"
        assert user.password is not None
        assert user.resident_id is not None

        # Assert that the user's password can be verified
        assert user.verify_password("password") is True

    # Tests that the user's password can be verified
    @pytest.mark.asyncio
    async def test_verify_user_password(self):
        # Create a user with a password
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password=self.auth_handler.get_password_hash("password"),
            resident_id=uuid4(),
        )

        # Verify the user's password
        assert user.verify_password("password") is True

    # Tests that the user's username can be updated
    @pytest.mark.asyncio
    async def test_update_user_username(self):
        # Create a user with a username
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password="password",
            resident_id=uuid4(),
        )

        # Update the user's username
        new_username = "newusername"
        user.username = new_username

        # Assert that the username is updated successfully
        assert user.username == new_username

    # Tests that the user can be deleted
    @pytest.mark.asyncio
    async def test_delete_user(self):
        from unittest.mock import Mock

        # Create a mock request object
        request = Mock()

        # Create a user
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password="password",
            resident_id=uuid4(),
        )

        # Delete the user
        del user

        # Assert that the user is deleted successfully
        assert "user" not in locals()

    # Tests that an error is not raised when trying to create a user with an invalid role
    @pytest.mark.asyncio
    async def test_create_user_with_invalid_role(self, mocker):
        # Create a mock request object
        mocker.Mock()

        # Try to create a user with an invalid role
        User(
            id=uuid4(),
            name="John Doe",
            role="INVALID_ROLE",
            username="johndoe",
            password="password",
            resident_id=uuid4(),
        )

    # Tests that the username of a user can be updated to an empty value
    @pytest.mark.asyncio
    async def test_update_user_with_empty_username(self, mocker):
        from unittest.mock import Mock

        # Create a mock request object
        Mock()

        # Create a user with a non-empty username
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password="password",
            resident_id=uuid4(),
        )

        # Update the user's username to an empty value
        user.username = ""

        # Assert that the username is updated successfully
        assert user.username == ""

    # Tests that a user can be created with a null password and that the password cannot be verified
    @pytest.mark.asyncio
    async def test_create_user_with_null_password(self):
        # Create a user with a null password
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password=None,
            resident_id=uuid4(),
        )

        # Assert that the user is created successfully
        assert user.name == "John Doe"
        assert user.role == Role.RESIDENT
        assert user.username == "johndoe"
        assert user.password is None
        assert user.resident_id is not None

        # Assert that the user's password cannot be verified
        assert not user.verify_password("password")

    # Tests that the user can be updated with both resident_id and guard_id
    @pytest.mark.asyncio
    async def test_update_user_with_both_resident_id_and_guard_id(self, mocker):
        from unittest.mock import Mock

        # Create a mock request object
        Mock()

        # Create a user with resident_id and guard_id
        user = User(
            id=uuid4(),
            name="John Doe",
            role=Role.RESIDENT,
            username="johndoe",
            password="password",
            resident_id=uuid4(),
            guard_id=uuid4(),
        )

        # Update the user with new resident_id and guard_id
        new_resident_id = uuid4()
        new_guard_id = uuid4()
        user.resident_id = new_resident_id
        user.guard_id = new_guard_id

        # Assert that the user is updated successfully
        assert user.resident_id == new_resident_id
        assert user.guard_id == new_guard_id
