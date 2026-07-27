from conftest import client


def create_camp(headers):
    response = client.post(
        "/camps",
        headers=headers,
        json={
            "camp_name": "Relief Camp",
            "location": "Chennai",
            "district": "Chennai",
            "capacity": 10,
            "available_capacity": 10,
            "status": "Active"
        }
    )

    return response.json()["id"]


def test_register_victim(coordinator_token):
    camp_id = create_camp(coordinator_token)

    response = client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "Rahul",
            "age": 30,
            "gender": "Male",
            "contact_number": "9876543210",
            "family_members": 4,
            "camp_id": camp_id
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Rahul"


def test_get_all_victims(coordinator_token):
    camp_id = create_camp(coordinator_token)

    client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "Priya",
            "age": 25,
            "gender": "Female",
            "contact_number": "9999999999",
            "family_members": 2,
            "camp_id": camp_id
        }
    )

    response = client.get(
        "/victims",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_victim_by_id(coordinator_token):
    camp_id = create_camp(coordinator_token)

    victim = client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "Arun",
            "age": 40,
            "gender": "Male",
            "contact_number": "8888888888",
            "family_members": 3,
            "camp_id": camp_id
        }
    )

    victim_id = victim.json()["id"]

    response = client.get(
        f"/victims/{victim_id}",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert response.json()["id"] == victim_id


def test_update_victim(coordinator_token):
    camp_id = create_camp(coordinator_token)

    victim = client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "Kumar",
            "age": 35,
            "gender": "Male",
            "contact_number": "7777777777",
            "family_members": 5,
            "camp_id": camp_id
        }
    )

    victim_id = victim.json()["id"]

    response = client.put(
        f"/victims/{victim_id}",
        headers=coordinator_token,
        json={
            "name": "Kumar Updated"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Kumar Updated"


def test_invalid_victim_id(coordinator_token):
    response = client.get(
        "/victims/999",
        headers=coordinator_token
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Victim not found."


def test_camp_full_validation(coordinator_token):
    response = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Small Camp",
            "location": "Madurai",
            "district": "Madurai",
            "capacity": 1,
            "available_capacity": 1,
            "status": "Active"
        }
    )

    camp_id = response.json()["id"]

    client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "First",
            "age": 20,
            "gender": "Male",
            "contact_number": "9000000001",
            "family_members": 1,
            "camp_id": camp_id
        }
    )

    second = client.post(
        "/victims",
        headers=coordinator_token,
        json={
            "name": "Second",
            "age": 22,
            "gender": "Female",
            "contact_number": "9000000002",
            "family_members": 2,
            "camp_id": camp_id
        }
    )

    assert second.status_code == 400
    assert second.json()["detail"] == "Camp is full."