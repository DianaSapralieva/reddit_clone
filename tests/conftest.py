from fastapi.testclient import TestClient
from v4_user.main import app
from v4_user.models import Base
from v4_user.database import get_db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL (Bad practice to put it here)
DATABASE_URL = "postgresql://postgres:API@localhost/reddit_clone_test"

#Running engine for ORM translation (python to SQL)
database_engine = create_engine(DATABASE_URL)

#session template for the connection
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=database_engine)

#Create and close session on-demand
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database session requirement
@pytest.fixture()
def session():
    #Clean DB by deleting the previous tables
    Base.metadata.drop_all(bind=database_engine)
    #Create all the tables again
    Base.metadata.create_all(bind=database_engine)
    #Override get_db (production by test db)
    app.dependency_overrides[get_db] = override_get_db


# fixture == requirement
@pytest.fixture()
def client(session): # before executing client fixture, execute the session fixture
    yield TestClient(app)


# Create User requirement
@pytest.fixture()
def created_user(client):
    user_credentials = {
        "email":"test.user@domain.lu", # need to be different than test_create_user
        "password":"1234"
    }
    res = client.post("/users", json=user_credentials)
    assert res.status_code == 201
    new_user = res.json()
    # add the password to the new_user data
    new_user["password"] = user_credentials["password"]
    return new_user

# GET THE CONSUMER TOKEN (REQUIREMENT)
@pytest.fixture()
def user_token(created_user, client):
    res = client.post("/auth/", data={"username": created_user["email"] , 
                                      "password": created_user["password"]})
    return res.json().get("access_token") #retrieve the access_token


# Authorized client (Requirement)
@pytest.fixture()
def authorized_client(client, user_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {user_token}"
    }
    return client

# Create blogpost requirement
@pytest.fixture
def created_post(authorized_client):
    authorized_client.post(
        "/posts/", json={"title": "My fixture title", "content": "My fixture content", "author":"test user"})