import pytest

from app.core.security import create_access_token
from app.db.database import SessionLocal
from app.models import User


@pytest.mark.parametrize("subject", [None, "invalid", "0", "-1"])
def test_invalid_token_subject_returns_401(client, subject):
    token = create_access_token({"sub": subject} if subject is not None else {})
    response = client.get("/documents/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_deactivated_user_cannot_use_an_existing_token(client):
    login = client.post("/auth/login", json={"username": "testadmin", "password": "test-admin-pw-strong"}).json()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "testadmin").one()
        user.is_active = False
        db.commit()
        response = client.get("/documents/", headers={"Authorization": f"Bearer {login['access_token']}"})
        assert response.status_code == 401
    finally:
        user.is_active = True
        db.commit()
        db.close()


@pytest.mark.parametrize("query", ["skip=-1", "limit=0", "limit=501"])
def test_pagination_is_bounded(client, query):
    login = client.post("/auth/login", json={"username": "testadmin", "password": "test-admin-pw-strong"}).json()
    response = client.get(f"/documents/?{query}", headers={"Authorization": f"Bearer {login['access_token']}"})
    assert response.status_code == 422


def test_nonexistent_document_history_returns_404(client):
    login = client.post("/auth/login", json={"username": "testadmin", "password": "test-admin-pw-strong"}).json()
    response = client.get("/documents/999999/history", headers={"Authorization": f"Bearer {login['access_token']}"})
    assert response.status_code == 404
