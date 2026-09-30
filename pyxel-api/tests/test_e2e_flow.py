import uuid


def unique_username():
    return f"e2e_{uuid.uuid4().hex[:8]}"


def test_full_user_journey_register_login_submit_score_appears_on_leaderboard(client):
    username = unique_username()
    password = "pass123"

    # 1. Register
    register_response = client.post("/register", json={"username": username, "password": password})
    assert register_response.status_code == 201
    token = register_response.get_json()["token"]

    # 2. Log in
    login_response = client.post("/login", json={"username": username, "password": password})
    assert login_response.status_code == 200
    login_token = login_response.get_json()["token"]

    # 3. Submit a score using the login token
    submit_response = client.post(
        "/submit-score",
        json={"score": 150},
        headers={"Authorization": f"Bearer {login_token}"}
    )
    assert submit_response.status_code == 200

    # 4. score appears on the leaderboard
    top_response = client.get("/top")
    assert top_response.status_code == 200
    leaderboard = top_response.get_json()
    assert [username, 150] in leaderboard


def test_submitting_score_without_token_is_rejected(client):
    response = client.post("/submit-score", json={"score": 100})
    assert response.status_code == 401
