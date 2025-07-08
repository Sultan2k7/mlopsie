import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

# Dummy user data
def user_payload(username, email, password):
    return {"username": username, "email": email, "password": password}

def test_create_user():
    response = client.post("/users/", json=user_payload("testuser", "test@example.com", "testpass"))
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user():
    # Create user first
    response = client.post("/users/", json=user_payload("getuser", "get@example.com", "getpass"))
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "getuser"
    assert data["email"] == "get@example.com"

def test_update_user():
    # Create user first
    response = client.post("/users/", json=user_payload("updateuser", "update@example.com", "updatepass"))
    user_id = response.json()["id"]
    update_data = user_payload("updated", "updated@example.com", "newpass")
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updated"
    assert data["email"] == "updated@example.com"

def test_delete_user():
    # Create user first
    response = client.post("/users/", json=user_payload("deluser", "del@example.com", "delpass"))
    user_id = response.json()["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    # Try to get deleted user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404

def test_get_user_posts():
    # Create user
    response = client.post("/users/", json=user_payload("postuser", "post@example.com", "postpass"))
    user_id = response.json()["id"]
    # No posts yet
    response = client.get(f"/users/{user_id}/posts")
    assert response.status_code == 200
    assert response.json() == [] 