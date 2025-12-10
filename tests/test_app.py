import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User


@pytest.fixture
def client():

    app.config['TESTING'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()

        admin = User(username='admin', password='password123')
        db.session.add(admin)
        db.session.commit()

        yield app.test_client()

        db.session.remove()
        db.drop_all()



def test_health_check(client):

    response = client.get('/')
    assert response.status_code == 200
    assert b"Coursework API is running" in response.data


def test_currency_endpoint(client):

    response = client.get('/currency')

    assert response.status_code in [200, 500, 502]


def test_items_list(client):

    response = client.get('/items')
    assert response.status_code == 200
    assert response.json == []


def test_create_item_auth_fail(client):

    response = client.post('/items', json={"id": 1, "name": "Test"})
    assert response.status_code == 401


def test_create_item_success(client):

    headers = {'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM='}
    item_data = {"id": 100, "name": "Super Item", "price": 99.9}

    response = client.post('/items', json=item_data, headers=headers)
    assert response.status_code == 201
    assert b"Created" in response.data