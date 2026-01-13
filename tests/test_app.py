from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_get_activities_returns_all_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Should return the same keys as the in-memory activities dict
    assert set(data.keys()) == set(activities.keys())


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure clean start state for this email
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_for_nonexistent_activity_returns_404():
    response = client.post(
        "/activities/UnknownActivity/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404


def test_signup_duplicate_participant_returns_400():
    activity_name = "Programming Class"
    email = "duplicate@mergington.edu"

    # Ensure the participant is already registered
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400


def test_unregister_participant_removes_participant():
    activity_name = "Gym Class"
    email = "leaving@mergington.edu"

    # Ensure the participant is present at the start
    if email not in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].append(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_returns_404():
    activity_name = "Soccer Team"
    email = "notregistered@mergington.edu"

    # Ensure the participant is not in the list
    if email in activities[activity_name]["participants"]:
        activities[activity_name]["participants"].remove(email)

    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    assert response.status_code == 404
