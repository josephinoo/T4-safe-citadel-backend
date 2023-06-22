from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@pytest.fixture(scope="module")
def testapp():
    return client


@pytest.mark.asyncio
async def test_login(testapp, monkeypatch):
    test_request_payload = {"username": "admin", "password": "admin"}
    test_response_payload = {"access_token": "string", "refresh_token": "string"}

    async def mock_login(username, password):
        return 1

    monkeypatch.setattr(
        "src.crud.login",
        AsyncMock(
            side_effect=lambda username, password: mock_login(username, password)
        ),
    )
    response = await testapp.post("/api/login", json=test_request_payload)
    assert response.status_code == 200
    assert response.json() == test_response_payload
