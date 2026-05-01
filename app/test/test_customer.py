from fastapi import status


def test_create_customer(client):
    response = client.post(
        "/customers",
        json={
            "name":"John Doe",
            "email": "john@example.com",
            "age": 33
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    
def test_read_customer(client):
    response = client.post(
        "/customers",
        json={
            "name":"John Doe",
            "email": "john@example.com",
            "age": 33
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    customer_id:int = response.json()['id']
    response_read = client.get(f"/customers/{customer_id}")
    
    assert response_read.json()['name'] == 'John Doe'
    assert response_read.status_code == status.HTTP_200_OK
    
    
def test_delete_customer(client):
    response = client.post(
        "/customers",
        json={
            "name":"John Doe",
            "email": "john@example.com",
            "age": 33
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    customer_id:int = response.json()['id']
    response_deleted = client.delete(f"/customers/{customer_id}")
    assert response_deleted.status_code == status.HTTP_204_NO_CONTENT
    
def test_update_customer(client):
    response = client.post(
        "/customers",
        json={
            "name":"John Doe",
            "email": "john@example.com",
            "age": 33
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    customer_id:int = response.json()['id']
    response_updated = client.patch(f"/customers/{customer_id}",json={'name':'Saul Perez'})
    
    assert response_updated.status_code == status.HTTP_200_OK
    assert response_updated.json()['name'] == 'Saul Perez'
    
    
def test_cannot_update_customer(client):
    response = client.post(
        "/customers",
        json={
            "name":"John Doe",
            "email": "john@example.com",
            "age": 33
        },
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    customer_id:int = 2
    response_updated = client.patch(f"/customers/{customer_id}",json={'name':'Saul Perez'})
    
    assert response_updated.status_code == status.HTTP_404_NOT_FOUND

def test_cannot_read_customer(client):
    response = client.post(
        "/customers",
        json={
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 33
            }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == 1;
    customer_id: int = 2
    response_read = client.get(f"/customers/{customer_id}")
    assert response_read.status_code == status.HTTP_404_NOT_FOUND