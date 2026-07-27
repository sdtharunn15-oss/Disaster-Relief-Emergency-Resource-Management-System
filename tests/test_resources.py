from conftest import client


def create_camp(headers):
    response = client.post(
        "/camps",
        headers=headers,
        json={
            "camp_name": "Resource Camp",
            "location": "Chennai",
            "district": "Chennai",
            "capacity": 100,
            "available_capacity": 100,
            "status": "Active"
        }
    )

    return response.json()["id"]


def test_create_resource(coordinator_token):
    camp_id = create_camp(coordinator_token)

    response = client.post(
        "/resources",
        headers=coordinator_token,
        json={
            "camp_id": camp_id,
            "resource_type": "Food",
            "stock": 100,
            "quantity": 20,
            "distributed_by": "Coordinator"
        }
    )

    assert response.status_code == 201
    assert response.json()["resource_type"] == "Food"


def test_get_all_resources(coordinator_token):
    camp_id = create_camp(coordinator_token)

    client.post(
        "/resources",
        headers=coordinator_token,
        json={
            "camp_id": camp_id,
            "resource_type": "Water",
            "stock": 100,
            "quantity": 50,
            "distributed_by": "Coordinator"
        }
    )

    response = client.get(
        "/resources",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_resource_by_id(coordinator_token):
    camp_id = create_camp(coordinator_token)

    resource = client.post(
        "/resources",
        headers=coordinator_token,
        json={
            "camp_id": camp_id,
            "resource_type": "Medicine",
            "stock": 200,
            "quantity": 40,
            "distributed_by": "Coordinator"
        }
    )

    resource_id = resource.json()["id"]

    response = client.get(
        f"/resources/{resource_id}",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert response.json()["id"] == resource_id


def test_resource_not_found(coordinator_token):
    response = client.get(
        "/resources/999",
        headers=coordinator_token
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resource not found."


def test_insufficient_stock(coordinator_token):
    camp_id = create_camp(coordinator_token)

    response = client.post(
        "/resources",
        headers=coordinator_token,
        json={
            "camp_id": camp_id,
            "resource_type": "Blankets",
            "stock": 10,
            "quantity": 20,
            "distributed_by": "Coordinator"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient stock."