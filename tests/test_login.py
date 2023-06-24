from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# create test login


async def test_login_unauthorized():
    response = client.post("/api/login/", json={"username": "foo", "password": "bar"})
    assert response.status_code == 401
