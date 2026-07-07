from datetime import date
from decimal import Decimal
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
    assert Decimal(json_response['amount']) == Decimal("5000")
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
    assert len(response.json()["items"]) == 1

    client.post("/expenses", json = {
        "title": "Prueba2",
        "amount": 7000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)

    response = client.get("/expenses", headers = auth_headers)
    assert len(response.json()["items"]) == 2

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
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["category"] == "food"
    assert response.json()["items"][0]["title"] == "Prueba1"


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
    assert len(response.json()["items"]) == 2
    response = client.get(f"/expenses/?date_to={today}", headers = auth_headers)
    assert len(response.json()["items"]) == 0


def test_get_single_expense(client, auth_headers):
    created = client.post("/expenses", json={
        "title": "Gasto único",
        "amount": 1500,
        "category": "food",
        "description": "desc"
    }, headers=auth_headers).json()

    response = client.get(f"/expenses/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["title"] == "Gasto único"


def test_get_single_expense_not_found(client, auth_headers):
    response = client.get("/expenses/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_expense(client, auth_headers):
    created = client.post("/expenses", json={
        "title": "Original",
        "amount": 1000,
        "category": "food",
        "description": ""
    }, headers=auth_headers).json()

    response = client.put(f"/expenses/{created['id']}", json={
        "title": "Modificado",
        "amount": 2000
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Modificado"
    assert Decimal(response.json()["amount"]) == Decimal("2000")
    assert response.json()["category"] == "food"  # sin cambios


def test_update_expense_not_found(client, auth_headers):
    response = client.put("/expenses/9999", json={"title": "x"}, headers=auth_headers)
    assert response.status_code == 404


def test_delete_expense(client, auth_headers):
    created = client.post("/expenses", json={
        "title": "A borrar",
        "amount": 500,
        "category": "other",
        "description": ""
    }, headers=auth_headers).json()

    response = client.delete(f"/expenses/{created['id']}", headers=auth_headers)
    assert response.status_code == 200

    response = client.get(f"/expenses/{created['id']}", headers=auth_headers)
    assert response.status_code == 404


def test_delete_expense_not_found(client, auth_headers):
    response = client.delete("/expenses/9999", headers=auth_headers)
    assert response.status_code == 404


def test_summary(client, auth_headers):
    client.post("/expenses", json={"title": "A", "amount": "3000.00", "category": "food", "description": ""}, headers=auth_headers)
    client.post("/expenses", json={"title": "B", "amount": "7000.00", "category": "transport", "description": ""}, headers=auth_headers)

    response = client.get("/expenses/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["total"]) == Decimal("10000")
    assert data["count"] == 2
    assert Decimal(data["average"]) == Decimal("5000")


def test_summary_empty(client, auth_headers):
    response = client.get("/expenses/summary", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["total"]) == Decimal("0")
    assert data["count"] == 0
    assert Decimal(data["average"]) == Decimal("0")


def test_summary_by_category(client, auth_headers):
    client.post("/expenses", json={"title": "A", "amount": "3000.00", "category": "food", "description": ""}, headers=auth_headers)
    client.post("/expenses", json={"title": "B", "amount": "7000.00", "category": "food", "description": ""}, headers=auth_headers)
    client.post("/expenses", json={"title": "C", "amount": "2000.00", "category": "transport", "description": ""}, headers=auth_headers)

    response = client.get("/expenses/summary/by-category", headers=auth_headers)
    assert response.status_code == 200
    totals = {item["category"]: item["total"] for item in response.json()}
    assert Decimal(totals["food"]) == Decimal("10000")
    assert Decimal(totals["transport"]) == Decimal("2000")


def test_pagination(client, auth_headers):
    for i in range(5):
        client.post("/expenses", json={
            "title": f"Gasto {i}",
            "amount": 1000,
            "category": "food",
            "description": ""
        }, headers=auth_headers)

    response = client.get("/expenses?skip=0&limit=2", headers=auth_headers)
    data = response.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["has_more"] is True

    response = client.get("/expenses?skip=4&limit=2", headers=auth_headers)
    data = response.json()
    assert len(data["items"]) == 1
    assert data["has_more"] is False


def test_expense_isolation(client, auth_headers):
    client.post("/expenses", json={
        "title": "Gasto usuario 1",
        "amount": 1000,
        "category": "food",
        "description": ""
    }, headers=auth_headers)

    client.post("/users/create", json={"username": "otrouser", "password": "otrapassword"})
    login = client.post("/users/login", data={"username": "otrouser", "password": "otrapassword"})
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = client.get("/expenses", headers=other_headers)
    assert response.json()["total"] == 0
    assert response.json()["items"] == []


def test_export_expenses_csv(client, auth_headers):
    client.post("/expenses", json={
        "title": "Comida",
        "amount": 5000,
        "category": "food",
        "description": "Almuerzo"
    }, headers=auth_headers)
    client.post("/expenses", json={
        "title": "Uber",
        "amount": 1500,
        "category": "transport",
        "description": ""
    }, headers=auth_headers)

    response = client.get("/expenses/export", headers=auth_headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
    assert "attachment; filename=expenses_" in response.headers["content-disposition"]
    assert ".csv" in response.headers["content-disposition"]

    lines = response.text.strip().split("\n")
    assert lines[0] == "id,title,amount,category,description,created_at"
    assert len(lines) == 3


def test_export_expenses_unauthorized(client):
    response = client.get("/expenses/export")
    assert response.status_code == 401

def test_top_category(client, auth_headers):
    expense = client.post("/expenses", json = {
        "title": "Prueba",
        "amount": 5678.89,
        "category": "food",
        "description": ""
    }, headers=auth_headers)
    response = client.get("/expenses/summary/top-category", headers = auth_headers)
    data = response.json()
    assert response.status_code == 200
    assert Decimal(data["total"]) == Decimal("5678.89")
    assert data["category"] == "food"
    
