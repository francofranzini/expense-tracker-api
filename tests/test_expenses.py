from datetime import date
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

def test_filter_by_category(client, auth_headers):
    client.post("/expenses", json = {
        "title": "Prueba1",
        "amount": 5000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)
    client.post("/expenses", json = {
        "title": "Prueba2",
        "amount": 5000,
        "category": "transport",
        "description": ""
    }, headers=auth_headers)
    response = client.get("/expenses/?category=food", headers = auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1                        
    assert response.json()[0]["category"] == "food"         
    assert response.json()[0]["title"] == "Prueba1"         


def test_filter_by_date(client, auth_headers):
    client.post("/expenses", json = {
        "title": "Prueba1",
        "amount": 5000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)
    client.post("/expenses", json = {
        "title": "Prueba2",
        "amount": 5000,
        "category": "transport",
        "description": ""
    }, headers=auth_headers)

    today = date.today()
    response = client.get(f"/expenses/?date_from={today}", headers = auth_headers)
    assert len(response.json()) == 2
    response = client.get(f"/expenses/?date_to={today}", headers = auth_headers)
    assert len(response.json()) == 0
    

