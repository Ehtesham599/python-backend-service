import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_hello_world_endpoint_returns_expected_message(client):
    response = client.get('/hello_world')

    assert response.status_code == 200
    assert response.get_json() == {'hello': 'world'}


def test_hello_endpoint_returns_greeting_for_valid_name(client):
    response = client.get('/hello?name=Alice')

    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, Alice!'}


def test_hello_endpoint_returns_400_when_name_is_missing(client):
    response = client.get('/hello')

    assert response.status_code == 400
    payload = response.get_json()
    assert 'error' in payload
    assert isinstance(payload['error'], list)


def test_hello_endpoint_returns_400_when_name_is_empty(client):
    response = client.get('/hello?name=')

    assert response.status_code == 400
    payload = response.get_json()
    assert 'error' in payload
    assert any(error.get('loc', []) == ['name'] for error in payload['error'])