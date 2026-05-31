import pytest
from fastapi.testclient import TestClient # type: ignore
from sqlalchemy import create_engine # type: ignore
from sqlalchemy.orm import sessionmaker # type: ignore
from app.main import app
from app.database import Base, get_db
import os

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)


#registered_user crea un cliente en la DB, usa el fixture
#client que le provee una interfaz httpx para el testing

@pytest.fixture
def registered_user(client):
    username = "testuser"
    password = "testpassword"
    client.post("/users/create", json = {
        "username": username,
        "password": password
    })
    return {"username": username, "password":password}

#auth_headers es un fixture que recibe un token a partir de los 2 fixtures declarados
#anteriormente. 
@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post("/users/login", data = {
        "username":registered_user["username"],
        "password":registered_user["password"]
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
