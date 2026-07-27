from conftest import client


def create_camp(headers):
    response = client.post(
        "/camps",
        headers=headers,
        json={
            "camp_name": "Report Camp",
            "location": "Chennai",
            "district": "Chennai",
            "capacity": 100,
            "available_capacity": 100,
            "status": "Active"
        }
    )

    return response.json()["id"]


def create_victim(headers, camp_id):
    client.post(
        "/victims",
        headers=headers,
        json={
            "name": "Rahul",
            "age": 30,
            "gender": "Male",
            "contact_number": "9876543210",
            "family_members": 4,
            "camp_id": camp_id
        }
    )


def create_resource(headers, camp_id):
    client.post(
        "/resources",
        headers=headers,
        json={
            "camp_id": camp_id,
            "resource_type": "Food",
            "stock": 100,
            "quantity": 20,
            "distributed_by": "Coordinator"
        }
    )


def create_volunteer(headers, camp_id):
    volunteer = client.post(
        "/volunteers",
        headers=headers,
        json={
            "name": "Volunteer",
            "email": "volunteer@gmail.com",
            "phone": "9876543210"
        }
    )

    volunteer_id = volunteer.json()["id"]

    client.post(
        f"/volunteers/{volunteer_id}/assign/{camp_id}",
        headers=headers
    )


def test_search_camp_by_district(coordinator_token):
    create_camp(coordinator_token)

    response = client.get(
        "/reports/search/camps?district=Chennai",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_filter_victims_by_camp(coordinator_token):
    camp_id = create_camp(coordinator_token)

    create_victim(coordinator_token, camp_id)

    response = client.get(
        f"/reports/filter/victims?camp_id={camp_id}",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_resource_distribution_history(coordinator_token):
    camp_id = create_camp(coordinator_token)

    create_resource(coordinator_token, camp_id)

    response = client.get(
        "/reports/history/resources",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_volunteer_assignments(coordinator_token):
    camp_id = create_camp(coordinator_token)

    create_volunteer(coordinator_token, camp_id)

    response = client.get(
        "/reports/volunteer-assignments",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_camp_pagination(coordinator_token):
    for i in range(15):
        client.post(
            "/camps",
            headers=coordinator_token,
            json={
                "camp_name": f"Camp {i}",
                "location": "Chennai",
                "district": "Chennai",
                "capacity": 100,
                "available_capacity": 100,
                "status": "Active"
            }
        )

    response = client.get(
        "/reports/search/camps?district=Chennai&page=1&limit=5",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) <= 5


def test_victim_pagination(coordinator_token):
    camp_id = create_camp(coordinator_token)

    for i in range(15):
        client.post(
            "/victims",
            headers=coordinator_token,
            json={
                "name": f"Victim {i}",
                "age": 25,
                "gender": "Male",
                "contact_number": f"99999999{i:02d}",
                "family_members": 2,
                "camp_id": camp_id
            }
        )

    response = client.get(
        f"/reports/filter/victims?camp_id={camp_id}&page=1&limit=5",
        headers=coordinator_token
    )

    assert response.status_code == 200
    assert len(response.json()) <= 5