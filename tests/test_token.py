from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app
from src.auth import AuthHandler

client = TestClient(app)


class TestToken:
    def test_valid_token(self, mocker):
        mocker.patch.object(
            AuthHandler, "verify_refresh_token", return_value={"sub": "1234"}
        )
        mocker.patch.object(
            AuthHandler, "create_access_token", return_value="new_token"
        )
        response = client.get("/api/refresh?token=valid_token")
        assert response.status_code == 200
        assert response.json() == {
            "access_token": "new_token",
            "token_type": "Bearer",
            "status": 200,
        }

    def test_invalid_token(self, mocker):
        mocker.patch.object(
            AuthHandler,
            "verify_refresh_token",
            side_effect=HTTPException(status_code=401, detail="Invalid token"),
        )
        response = client.get("/api/refresh?token=invalid_token")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token"}

    def test_expired_token(self, mocker):
        mocker.patch.object(
            AuthHandler,
            "verify_refresh_token",
            side_effect=HTTPException(status_code=401, detail="Token has expired"),
        )
        response = client.get("/api/refresh?token=expired_token")
        assert response.status_code == 401
        assert response.json() == {"detail": "Token has expired"}

    def test_invalid_signature_token(self, mocker):
        mocker.patch.object(
            AuthHandler,
            "verify_refresh_token",
            side_effect=HTTPException(
                status_code=401, detail="Invalid token signature"
            ),
        )
        response = client.get("/api/refresh?token=invalid_signature_token")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token signature"}

    def test_invalid_format_token(self, mocker):
        mocker.patch.object(
            AuthHandler,
            "verify_refresh_token",
            side_effect=HTTPException(status_code=401, detail="Invalid token format"),
        )
        response = client.get("/api/refresh?token=invalid_format_token")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token format"}

    def test_wrong_audience_token(self, mocker):
        mocker.patch.object(
            AuthHandler,
            "verify_refresh_token",
            side_effect=HTTPException(status_code=401, detail="Invalid audience"),
        )
        response = client.get("/api/refresh?token=wrong_audience_token")
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid audience"}
