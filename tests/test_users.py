from jose import jwt
from v4_user.utilities.jwt_manager import SERVER_KEY, ALGORITHM
import pytest


#test the creation of an User
def test_create_user(client):
    response = client.post("/users/", json={"email": "user@example.com", "password" : "1234"})
    assert response.json().get("email") == "user@example.com"
    assert response.status_code == 201


def test_login_user(created_user, client):
    res= client.post("/auth/", data={"username": created_user["email"],
                                     "password": created_user["password"]})
    assert res.status_code == 200
    assert res.json().get("token_type") == "bearer"
    # Verify the Token data
    payload = jwt.decode(res.json().get("access_token"), 
                         SERVER_KEY, algorithms=[ALGORITHM])
    id = payload.get("user_id")
    assert id == created_user["id"]


@pytest.mark.parametrize("email, password, status_code", [
    (None, "1234", 422),  # No email provided
    ("test.user@domain.lu", None, 422),  # No password provided
    ("wrongemail@gmail.com","1234", 401),  # wrong email
    ("test.user@domain.lu", "wrongpassword", 401), # wrong password
    ("wrongemail@gmail.com", "wrongpassword", 401) # wrong email + wrong password
])
def test_incorrect_credentials(client, created_user, email, password, status_code):
    response = client.post("/auth", data={"username": email, "password": password })
    assert response.status_code == status_code