import pytest
from fastapi.testclient import TestClient
from datetime import datetime, time
from src.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "id": "test_user1",
        "name": "Test User",
        "habits": [],
        "preferred_notification_time": "09:00:00",
        "timezone": "UTC",
        "created_at": "2024-04-02T12:00:00"
    }

@pytest.fixture
def test_habit():
    return {
        "id": "test_habit1",
        "name": "Morning Exercise",
        "description": "30 minutes of exercise",
        "frequency": "daily",
        "target_time": "07:00:00",
        "created_at": "2024-04-02T12:00:00",
        "difficulty": 3,
        "category": "health"
    }

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "features" in data
    assert len(data["features"]) > 0

def test_create_and_get_user(test_user):
    # Create user
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["id"] == test_user["id"]
    
    # Get user
    response = client.get(f"/users/{test_user['id']}")
    assert response.status_code == 200
    retrieved_user = response.json()
    assert retrieved_user["id"] == test_user["id"]

def test_create_and_get_habit(test_habit):
    # Create habit
    response = client.post("/habits/", json=test_habit)
    assert response.status_code == 200
    created_habit = response.json()
    assert created_habit["id"] == test_habit["id"]
    
    # Get habit
    response = client.get(f"/habits/{test_habit['id']}")
    assert response.status_code == 200
    retrieved_habit = response.json()
    assert retrieved_habit["id"] == test_habit["id"]

def test_record_completion(test_habit):
    # First create the habit
    client.post("/habits/", json=test_habit)
    
    # Record completion
    completion = {
        "habit_id": test_habit["id"],
        "completed_at": "2024-04-02T12:00:00",
        "notes": "Great workout!",
        "mood": 5,
        "difficulty": 2
    }
    
    response = client.post("/completions/", json=completion)
    assert response.status_code == 200
    recorded_completion = response.json()
    assert recorded_completion["habit_id"] == test_habit["id"]

def test_get_analytics(test_user, test_habit):
    # Create user and habit
    client.post("/users/", json=test_user)
    client.post("/habits/", json=test_habit)
    
    # Get analytics
    response = client.get(f"/analytics/{test_user['id']}")
    assert response.status_code == 200
    analytics = response.json()
    assert "total_habits" in analytics
    assert "average_success_rate" in analytics
    assert "total_streaks" in analytics
    assert "habits_by_category" in analytics

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    health = response.json()
    assert "status" in health
    assert health["status"] == "healthy"
    assert "users_count" in health
    assert "habits_count" in health
    assert "completions_count" in health 