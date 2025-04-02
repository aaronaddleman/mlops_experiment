import pytest
from flask import Flask
from src.ui import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Habit Wizard UI' in response.data

def test_agent_control(client):
    response = client.post('/control', json={
        'action': 'start',
        'frequency': 10
    })
    assert response.status_code == 200
    assert b'success' in response.data.lower()

def test_get_logs(client):
    response = client.get('/logs')
    assert response.status_code == 200
    assert isinstance(response.json, list) 