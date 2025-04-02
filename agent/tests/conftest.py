import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def clean_state():
    """Clean up the in-memory state before each test"""
    from src.main import users, habits, completions
    users.clear()
    habits.clear()
    completions.clear()
    yield 