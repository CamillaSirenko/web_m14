from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.models import Contact
from main import app
from src.routes.contacts import router
from src.schemas import ContactCreateUpdate, ContactResponse
from datetime import date, timedelta
import pytest

client = TestClient(app)

@pytest.fixture
def mock_get_current_user(monkeypatch):
    def mock_get_current_user():
        return Contact(id=1, user_id=1, firstname="John", lastname="Doe", email="john@example.com", phone="123456")

    monkeypatch.setattr("src.routes.contacts.auth_service.get_current_user", mock_get_current_user)

def test_create_contact(client: TestClient, mock_get_current_user, db_session: Session):
    contact_data = {
        "firstname": "Alice",
        "lastname": "Wonderland",
        "email": "alice@example.com",
        "phone": "789012",
        "birthday": str(date.today() + timedelta(days=30)),
    }

    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == contact_data["firstname"]
    assert data["lastname"] == contact_data["lastname"]
    assert data["email"] == contact_data["email"]
    assert data["phone"] == contact_data["phone"]
    assert "id" in data

def test_upcoming_birthdays(client: TestClient, db_session: Session):
    response = client.get("/upcoming_birthdays/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_contact(client: TestClient, db_session: Session):
    contact_id = 1

    response = client.get(f"/contacts/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id

def test_update_contact(client: TestClient, mock_get_current_user, db_session: Session):
    contact_id = 1

    updated_data = {
        "firstname": "UpdatedFirstName",
        "lastname": "UpdatedLastName",
        "email": "updated@example.com",
        "phone": "987654",
    }

    response = client.put(f"/contacts/{contact_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id
    assert data["firstname"] == updated_data["firstname"]
    assert data["lastname"] == updated_data["lastname"]
    assert data["email"] == updated_data["email"]
    assert data["phone"] == updated_data["phone"]

def test_delete_contact(client: TestClient, mock_get_current_user, db_session: Session):
    contact_id = 1

    response = client.delete(f"/contacts/{contact_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == contact_id