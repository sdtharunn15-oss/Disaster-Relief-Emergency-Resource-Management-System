import os
import sys
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.main import app
from app.database import Base, get_db


TEST_DATABASE_URL = "sqlite:///./test.db"

if os.path.exists("test.db"):
    os.remove("test.db")


engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def admin_token(session):

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

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def coordinator_token(session):

    client.post(
        "/auth/register",
        json={
            "username": "coordinator",
            "email": "coordinator@gmail.com",
            "password": "admin123",
            "role": "Relief Coordinator"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "coordinator@gmail.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture()
def volunteer_token(session):

    client.post(
        "/auth/register",
        json={
            "username": "volunteer",
            "email": "volunteer@gmail.com",
            "password": "admin123",
            "role": "Volunteer"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "volunteer@gmail.com",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }