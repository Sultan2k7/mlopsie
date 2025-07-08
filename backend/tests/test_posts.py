import pytest
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app

client = TestClient(app)

def user_payload(username, email, password):
    return {"username": username, "email": email, "password": password}

def post_payload(title, content):
    return {"title": title, "content": content}

def create_user_and_get_id(username, email, password):
    response = client.post("/users/", json=user_payload(username, email, password))
    return response.json()["id"]

def test_create_post():
    user_id = create_user_and_get_id("postuser1", "postuser1@example.com", "pass")
    response = client.post(f"/posts/?user_id={user_id}", json=post_payload("Test Post", "Test Content"))
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Test Content"
    assert data["user_id"] == user_id

def test_get_post():
    user_id = create_user_and_get_id("postuser2", "postuser2@example.com", "pass")
    response = client.post(f"/posts/?user_id={user_id}", json=post_payload("Get Post", "Content"))
    post_id = response.json()["id"]
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Post"
    assert data["user_id"] == user_id

def test_update_post():
    user_id = create_user_and_get_id("postuser3", "postuser3@example.com", "pass")
    response = client.post(f"/posts/?user_id={user_id}", json=post_payload("Old Title", "Old Content"))
    post_id = response.json()["id"]
    update_data = post_payload("New Title", "New Content")
    response = client.put(f"/posts/{post_id}?user_id={user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New Content"

def test_delete_post():
    user_id = create_user_and_get_id("postuser4", "postuser4@example.com", "pass")
    response = client.post(f"/posts/?user_id={user_id}", json=post_payload("Delete Me", "Bye"))
    post_id = response.json()["id"]
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 204
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 404

def test_get_posts_by_user():
    user_id = create_user_and_get_id("postuser5", "postuser5@example.com", "pass")
    # Create two posts for this user
    client.post(f"/posts/?user_id={user_id}", json=post_payload("Title1", "Content1"))
    client.post(f"/posts/?user_id={user_id}", json=post_payload("Title2", "Content2"))
    response = client.get(f"/posts/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_pagination():
    user_id = create_user_and_get_id("postuser6", "postuser6@example.com", "pass")
    # Create 15 posts
    for i in range(15):
        client.post(f"/posts/?user_id={user_id}", json=post_payload(f"Title{i}", f"Content{i}"))
    response = client.get("/posts/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    response = client.get("/posts/?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5 