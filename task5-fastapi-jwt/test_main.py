from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_register():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201


def test_login():
    client.post(
        "/register",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/login",
        json={
            "username": "loginuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_protected_endpoint_without_token():
    response = client.get("/items")

    assert response.status_code == 401
