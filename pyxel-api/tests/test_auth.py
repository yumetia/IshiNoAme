import uuid


def unique_username():
    # avoids collisions
    return f"test_{uuid.uuid4().hex[:8]}"


def test_register_should_return_token_for_new_username(client):
    username = unique_username()
    response = client.post("/register", json={"username": username, "password": "pass123"})

    assert response.status_code == 201
    assert "token" in response.get_json()


def test_register_should_reject_duplicate_username(client):
    username = unique_username()
    client.post("/register", json={"username": username, "password": "pass123"})

    response = client.post("/register", json={"username": username, "password": "pass123"})

    assert response.status_code == 409
    assert "error" in response.get_json()


def test_login_should_return_token_for_valid_credentials(client):
    username = unique_username()
    client.post("/register", json={"username": username, "password": "pass123"})

    response = client.post("/login", json={"username": username, "password": "pass123"})

    assert response.status_code == 200
    assert "token" in response.get_json()


def test_login_should_reject_wrong_password(client):
    username = unique_username()
    client.post("/register", json={"username": username, "password": "pass123"})

    response = client.post("/login", json={"username": username, "password": "wrongpass"})

    assert response.status_code == 401
    assert "error" in response.get_json()


def test_login_should_reject_unknown_username(client):
    response = client.post("/login", json={"username": "does_not_exist_xyz", "password": "pass123"})

    assert response.status_code == 401
    assert "error" in response.get_json()
    