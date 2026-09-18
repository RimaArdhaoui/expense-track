import os
import tempfile

import pytest

from app import create_app
from app.db import init_db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path, "SECRET_KEY": "test"})

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, username="alice", password="hunter2pass"):
    return client.post(
        "/register", data={"username": username, "password": password}
    )


def login(client, username="alice", password="hunter2pass"):
    return client.post(
        "/login", data={"username": username, "password": password}
    )


def test_register_and_login(client):
    r = register(client)
    assert r.status_code == 302  # redirect to login

    r = login(client)
    assert r.status_code == 302  # redirect to dashboard


def test_login_wrong_password_fails(client):
    register(client)
    r = login(client, password="wrong-password")
    assert r.status_code == 200  # re-renders login with a flash error


def test_dashboard_requires_login(client):
    r = client.get("/")
    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_add_expense(client):
    register(client)
    login(client)

    r = client.post(
        "/expenses/add",
        data={"amount": "12.50", "category": "Food", "note": "lunch"},
    )
    assert r.status_code == 302

    r = client.get("/")
    assert b"Food" in r.data
    assert b"12.50" in r.data


def test_api_expenses_json(client):
    register(client)
    login(client)
    client.post(
        "/expenses/add",
        data={"amount": "5", "category": "Transport", "note": ""},
    )

    r = client.get("/api/expenses")
    assert r.status_code == 200
    data = r.get_json()
    assert len(data) == 1
    assert data[0]["category"] == "Transport"
