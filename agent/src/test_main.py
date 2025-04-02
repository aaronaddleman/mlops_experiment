import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.database import get_db, Base, engine
from sqlalchemy.orm import Session
import uuid
from datetime import datetime, time

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = Session(engine)
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

def test_create_user(client):
    user_id = str(uuid.uuid4())
    response = client.post("/users/", json={
        "id": user_id,
        "name": "Test User",
        "habits": [],
        "preferred_notification_time": "09:00:00",
        "timezone": "UTC",
        "created_at": datetime.utcnow().isoformat()
    })
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_create_habit(client):
    # First create a user
    user_id = str(uuid.uuid4())
    client.post("/users/", json={
        "id": user_id,
        "name": "Test User",
        "habits": [],
        "preferred_notification_time": "09:00:00",
        "timezone": "UTC",
        "created_at": datetime.utcnow().isoformat()
    })
    
    # Then create a habit
    response = client.post(f"/habits/?user_id={user_id}", json={
        "id": str(uuid.uuid4()),
        "name": "Test Habit",
        "description": "A test habit",
        "frequency": "daily",
        "target_time": "09:00:00",
        "created_at": datetime.utcnow().isoformat(),
        "difficulty": 3,
        "category": "health"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Habit"

def test_get_analytics_empty(client):
    user_id = str(uuid.uuid4())
    response = client.get(f"/analytics/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_habits"] == 0
    assert data["average_success_rate"] == 0.0
    assert data["total_streaks"] == 0
    assert data["habits_by_category"] == {} 