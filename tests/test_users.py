def test_register_and_login_user(client):
    register_response = client.post(
        "/users/register",
        json={"username": "jane", "email": "jane@example.com", "password": "password123"},
    )
    assert register_response.status_code == 201
    user = register_response.json()
    assert user["email"] == "jane@example.com"
    assert "hashed_password" not in user

    login_response = client.post(
        "/users/login",
        json={"email": "jane@example.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["user"]["email"] == "jane@example.com"


def test_login_rejects_invalid_password(client):
    client.post(
        "/users/register",
        json={"username": "john", "email": "john@example.com", "password": "password123"},
    )
    response = client.post(
        "/users/login",
        json={"email": "john@example.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_register_validates_payload(client):
    response = client.post(
        "/users/register",
        json={"username": "ab", "email": "not-an-email", "password": "short"},
    )
    assert response.status_code == 422
