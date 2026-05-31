def test_create_expense(client, auth_headers):
    response = client.post("/expenses", json = {
        "title": "Prueba",
        "amount": 5000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)
    json_response = response.json()
    assert response.status_code == 200
    assert json_response['category'] == "food"
    assert json_response['amount'] == 5000
    assert json_response['description'] == ""
    assert json_response['title'] == "Prueba"

def test_get_expenses(client, auth_headers):
    client.post("/expenses", json = {
        "title": "Prueba1",
        "amount": 5000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)

    response = client.get("/expenses", headers = auth_headers)
    assert len(response.json()) == 1

    client.post("/expenses", json = {
        "title": "Prueba2",
        "amount": 7000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)

    response = client.get("/expenses", headers = auth_headers)
    assert len(response.json()) == 2

def test_unauthorized_access(client):
    response = client.post("/expenses", json = {
        "title": "Prueba",
        "amount": 5000,
        "category": "food",
        "description": ""
    })
    assert response.status_code == 401
    response = client.get("/expenses")
    assert response.status_code == 401