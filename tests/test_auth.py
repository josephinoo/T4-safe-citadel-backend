import datetime
from datetime import timedelta

import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.auth import AuthHandler


class TestAuthHandler:
    # Tests that get_password_hash returns a hashed password
    def test_get_password_hash_returns_hashed_password(self):
        # Arrange
        auth_handler = AuthHandler()
        password = "password123"

        # Act
        hashed_password = auth_handler.get_password_hash(password)

        # Assert
        assert hashed_password != password

    # Tests that verify_password returns True for correct password
    def test_verify_password_returns_true_for_correct_password(self):
        # Arrange
        auth_handler = AuthHandler()
        password = "password123"
        hashed_password = auth_handler.get_password_hash(password)

        # Act
        result = auth_handler.verify_password(password, hashed_password)

        # Assert
        assert result is True

    # Tests that encode_token returns a JWT token
    def test_encode_token_returns_jwt_token(self):
        # Arrange
        auth_handler = AuthHandler()
        user_id = "123"

        # Act
        token = auth_handler.encode_token(user_id)

        # Assert
        assert isinstance(token, str)

    # Tests that decode_token returns user ID for valid token
    def test_decode_token_returns_user_id_for_valid_token(self):
        # Arrange
        auth_handler = AuthHandler()
        user_id = "123"
        token = auth_handler.encode_token(user_id)

        # Act
        decoded_user_id = auth_handler.decode_token(token)

        # Assert
        assert decoded_user_id == user_id

    # Tests that auth_wrapper returns user ID for valid token
    def test_auth_wrapper_returns_user_id_for_valid_token(self):
        # Arrange
        auth_handler = AuthHandler()
        user_id = "123"
        token = auth_handler.encode_token(user_id)
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        # Act
        decoded_user_id = auth_handler.auth_wrapper(auth=credentials)

        # Assert
        assert decoded_user_id == user_id

    # Tests that refresh_token returns a refreshed JWT token
    def test_refresh_token_returns_refreshed_jwt_token(self):
        # Arrange
        auth_handler = AuthHandler()
        user_id = "123"
        original_token = auth_handler.encode_token(user_id)

        # Act
        refreshed_token = auth_handler.refresh_token(original_token)
        # Assert
        assert (
            refreshed_token == original_token
        ), "Refreshed token should not be the same as the original token"

    # Tests that create_access_token method in AuthHandler class returns an access token
    def test_create_access_token_returns_access_token(self):
        # Arrange
        auth_handler = AuthHandler()
        payload = {
            "sub": "user123",
            "exp": datetime.datetime.now() + timedelta(days=0, minutes=20),
            "iat": datetime.datetime.now(),
        }

        # Act
        access_token = auth_handler.create_access_token(payload)

        # Assert
        assert isinstance(access_token, str)

    # Tests that verify_password returns False when the provided password is incorrect
    def test_verify_password_returns_false_for_incorrect_password(self):
        # Arrange
        auth_handler = AuthHandler()
        hashed_password = auth_handler.get_password_hash("password123")
        incorrect_password = "incorrect"

        # Act
        result = auth_handler.verify_password(incorrect_password, hashed_password)

        # Assert
        assert result is False

    # Test that the verify_refresh_token method raises an HTTPException when the token is expired
    def test_verify_refresh_token_raises_exception_for_expired_token(self):
        # Arrange
        auth_handler = AuthHandler()
        expired_token = jwt.encode(
            {"exp": datetime.datetime.now() - timedelta(days=1)},
            auth_handler.secret,
            algorithm="HS256",
        )

        # Act and Assert
        with pytest.raises(HTTPException):
            auth_handler.verify_refresh_token(expired_token)

    # Test that the verify_refresh_token method raises an HTTPException when given an invalid token
    def test_verify_refresh_token_raises_HTTPException_for_invalid_token(self):
        # Arrange
        auth_handler = AuthHandler()
        invalid_token = "invalid_token"

        # Act and Assert
        with pytest.raises(HTTPException):
            auth_handler.verify_refresh_token(invalid_token)

    # Tests that verify_password returns False when an empty password is provided
    def test_verify_password_returns_false_for_empty_password(self):
        # Arrange
        auth_handler = AuthHandler()
        plain_password = ""
        hashed_password = auth_handler.get_password_hash("password123")

        # Act
        result = auth_handler.verify_password(plain_password, hashed_password)

        # Assert
        assert result is False
