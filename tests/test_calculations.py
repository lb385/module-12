def register_and_login(client):
    client.post(
        "/users/register",
        json={"username": "sam", "email": "sam@example.com", "password": "password123"},
    )
    login_response = client.post(
        "/users/login",
        json={"email": "sam@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_calculation_crud_flow(client):
    headers = register_and_login(client)

    create_response = client.post(
        "/calculations",
        json={"operand1": 10, "operand2": 5, "operation": "div"},
        headers=headers,
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["result"] == 2
    calculation_id = created["id"]

    list_response = client.get("/calculations", headers=headers)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    read_response = client.get(f"/calculations/{calculation_id}", headers=headers)
    assert read_response.status_code == 200
    assert read_response.json()["operation"] == "div"

    update_response = client.put(
        f"/calculations/{calculation_id}",
        json={"operand1": 12, "operand2": 3, "operation": "mul"},
        headers=headers,
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["result"] == 36

    delete_response = client.delete(f"/calculations/{calculation_id}", headers=headers)
    assert delete_response.status_code == 204

    missing_response = client.get(f"/calculations/{calculation_id}", headers=headers)
    assert missing_response.status_code == 404


def test_calculation_validates_and_blocks_invalid_values(client):
    headers = register_and_login(client)

    invalid_response = client.post(
        "/calculations",
        json={"operand1": 10, "operand2": 0, "operation": "div"},
        headers=headers,
    )
    assert invalid_response.status_code == 400
    assert invalid_response.json()["detail"] == "Division by zero is not allowed"

    schema_response = client.post(
        "/calculations",
        json={"operand1": 10, "operand2": 5, "operation": "pow"},
        headers=headers,
    )
    assert schema_response.status_code == 422
