from conftest import client


def test_create_camp(coordinator_token):
    response = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Chennai Relief Camp",
            "location": "Anna Nagar",
            "district": "Chennai",
            "capacity": 100,
            "available_capacity": 100,
            "status": "Active"
        }
    )

    assert response.status_code == 201
    assert response.json()["camp_name"] == "Chennai Relief Camp"


def test_get_all_camps(coordinator_token):
    client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Camp A",
            "location": "Velachery",
            "district": "Chennai",
            "capacity": 50,
            "available_capacity": 50,
            "status": "Active"
        }
    )

    response = client.get(
        "/camps",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_camp_by_id(coordinator_token):
    create = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Camp B",
            "location": "Tambaram",
            "district": "Chennai",
            "capacity": 75,
            "available_capacity": 75,
            "status": "Active"
        }
    )

    camp_id = create.json()["id"]

    response = client.get(
        f"/camps/{camp_id}",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert response.json()["id"] == camp_id


def test_update_camp(coordinator_token):
    create = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Old Camp",
            "location": "Avadi",
            "district": "Chennai",
            "capacity": 80,
            "available_capacity": 80,
            "status": "Active"
        }
    )

    camp_id = create.json()["id"]

    response = client.put(
        f"/camps/{camp_id}",
        headers=coordinator_token,
        json={
            "camp_name": "Updated Camp"
        }
    )

    assert response.status_code == 200
    assert response.json()["camp_name"] == "Updated Camp"


def test_delete_camp(coordinator_token):
    create = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Delete Camp",
            "location": "Porur",
            "district": "Chennai",
            "capacity": 60,
            "available_capacity": 60,
            "status": "Active"
        }
    )

    camp_id = create.json()["id"]

    response = client.delete(
        f"/camps/{camp_id}",
        headers=coordinator_token
    )

    assert response.status_code == 204


def test_get_invalid_camp(coordinator_token):
    response = client.get(
        "/camps/999",
        headers=coordinator_token
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Camp not found."