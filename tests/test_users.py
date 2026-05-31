 

def test_create_user(client):
    response = client.post("/users/create", json = {
        "username":"test1",
        "password":"pass1"
    })
    assert response.status_code == 200
    assert response.json()['username'] == 'test1'
    

def test_create_duplicate_user(client):
    response = client.post("/users/create", json = {
        "username":"test1",
        "password":"pass1"
    })
    response2 = client.post("/users/create", json = {
        "username":"test1",
        "password":"pass2"
    })
    assert response.status_code == 200
    assert response.json()['username'] == 'test1'
    assert response2.status_code == 400
