from sqlalchemy import select

from cloudwalk.db.models import Client


def test_read_root(test_client):
    response = test_client.get('/ping')
    assert response.status_code == 200
    assert response.json() == {'message': 'pong'}


def test_create_client(test_client):
    response = test_client.post(
        '/users/',
        json={
            'status': 'approved',
            'batch': 1,
            'credit_limit': 100000,
            'interest_rate': 20,
        },
    )

    assert response.status_code == 201
    assert response.json()['user_id'] == 1
    assert response.json()['status'] == 'approved'


def test_create_client_with_wrong_data(test_client):
    response = test_client.post(
        '/users/', json={'status': 'approved', 'batch': 1, 'interest_rate': 20}
    )

    assert response.status_code == 422


def test_update_client(test_client, approved_client, session):
    credit_limit = 100000
    response = test_client.put(
        f'/users/{approved_client.user_id}/',
        json={
            'status': 'approved',
            'batch': 1,
            'credit_limit': credit_limit,
            'interest_rate': 20,
        },
    )

    session.refresh(approved_client)

    assert response.status_code == 200
    assert approved_client.credit_limit == credit_limit


def test_update_client_with_wrong_data(test_client, approved_client):
    credit_limit = 100000
    response = test_client.put(
        f'/users/{approved_client.user_id}/',
        json={'batch': 1, 'credit_limit': credit_limit, 'interest_rate': 20},
    )
    assert response.status_code == 422


def test_update_client_does_not_exists(test_client):
    credit_limit = 100000
    response = test_client.put(
        f'/users/1',
        json={
            'status': 'approved',
            'batch': 1,
            'credit_limit': credit_limit,
            'interest_rate': 20,
        },
    )
    assert response.status_code == 404


def test_delete_client(test_client, approved_client, session):
    response = test_client.delete(f'/users/{approved_client.user_id}/')
    deleted_client = session.scalar(
        select(Client).where(Client.user_id == approved_client.user_id)
    )
    assert response.status_code == 200
    assert deleted_client == None


def test_delete_client_does_not_exists(test_client):
    response = test_client.delete(f'/users/1')
    assert response.status_code == 404
