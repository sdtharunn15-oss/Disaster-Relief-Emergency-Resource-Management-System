from conftest import client


def create_camp(headers):
    response = client.post(
        "/camps",
        headers=headers,
        json={
            "camp_name": "Volunteer Camp",
            "location": "Chennai",
            "district": "Chennai",
            "capacity": 100,
            "available_capacity": 100,
            "status": "Active"
        }
    )

    return response.json()["id"]


def test_create_volunteer(coordinator_token):
    response = client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Ravi",
            "email": "ravi@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Ravi"


def test_duplicate_volunteer_email(coordinator_token):
    client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Ravi",
            "email": "ravi@gmail.com",
            "phone": "9876543210"
        }
    )

    response = client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Ravi2",
            "email": "ravi@gmail.com",
            "phone": "9999999999"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Volunteer email already exists."


def test_get_all_volunteers(coordinator_token):
    client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Volunteer One",
            "email": "vol1@gmail.com",
            "phone": "9000000001"
        }
    )

    response = client.get(
        "/volunteers",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_assign_volunteer(coordinator_token):
    camp_id = create_camp(coordinator_token)

    volunteer = client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Suresh",
            "email": "suresh@gmail.com",
            "phone": "8888888888"
        }
    )

    volunteer_id = volunteer.json()["id"]

    response = client.post(
        f"/volunteers/{volunteer_id}/assign/{camp_id}",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Volunteer assigned successfully."


def test_assign_already_assigned_volunteer(coordinator_token):
    camp1 = create_camp(coordinator_token)

    camp2 = client.post(
        "/camps",
        headers=coordinator_token,
        json={
            "camp_name": "Camp Two",
            "location": "Madurai",
            "district": "Madurai",
            "capacity": 100,
            "available_capacity": 100,
            "status": "Active"
        }
    ).json()["id"]

    volunteer = client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Kumar",
            "email": "kumar@gmail.com",
            "phone": "7777777777"
        }
    )

    volunteer_id = volunteer.json()["id"]

    client.post(
        f"/volunteers/{volunteer_id}/assign/{camp1}",
        headers=coordinator_token
    )

    response = client.post(
        f"/volunteers/{volunteer_id}/assign/{camp2}",
        headers=coordinator_token
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Volunteer already assigned to another active camp."


def test_assign_invalid_volunteer(coordinator_token):
    camp_id = create_camp(coordinator_token)

    response = client.post(
        f"/volunteers/999/assign/{camp_id}",
        headers=coordinator_token
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Volunteer not found."


def test_assign_invalid_camp(coordinator_token):
    volunteer = client.post(
        "/volunteers",
        headers=coordinator_token,
        json={
            "name": "Arun",
            "email": "arun@gmail.com",
            "phone": "6666666666"
        }
    )

    volunteer_id = volunteer.json()["id"]

    response = client.post(
        f"/volunteers/{volunteer_id}/assign/999",
        headers=coordinator_token
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Camp not found."