from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# create test login


async def test_login_unauthorized():
    response = client.post("/api/login/", json={"username": "foo", "password": "bar"})
    assert response.status_code == 401


async def test_login_authorized(mocker):
    mocker.patch(
        "src.crud.login",
        return_value={"token": "token", "refresh_token": "refresh_token"},
    )
    response = client.post("/api/login/", json={"username": "foo", "password": "bar"})
    assert response.status_code == 200
    assert response.json() == {"token": "token", "refresh_token": "refresh_token"}
