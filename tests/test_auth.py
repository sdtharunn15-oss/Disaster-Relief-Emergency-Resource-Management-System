from conftest import client


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "email": "john@gmail.com",
            "password": "john123",
            "role": "Admin"
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully."


def test_duplicate_email():
    client.post(
        "/auth/register",
        json={
            "username": "john",
            "email": "john@gmail.com",
            "password": "john123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "john2",
            "email": "john@gmail.com",
            "password": "john123",
            "role": "Admin"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered."


def test_login_success():
    client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@gmail.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "admin@gmail.com",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "wrong@gmail.com",
            "password": "wrong123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password."