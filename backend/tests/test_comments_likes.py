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

def comment_payload(content):
    return {"content": content}

def create_user_and_get_id(username, email, password):
    response = client.post("/users/", json=user_payload(username, email, password))
    return response.json()["id"]

def create_post_and_get_id(user_id, title, content):
    response = client.post(f"/posts/?user_id={user_id}", json=post_payload(title, content))
    return response.json()["id"]

# Likes tests
def test_like_post():
    user_id = create_user_and_get_id("likeuser1", "likeuser1@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Like Test Post", "Content")
    response = client.post(f"/posts/{post_id}/like?user_id={user_id}")
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["post_id"] == post_id

def test_unlike_post():
    user_id = create_user_and_get_id("likeuser2", "likeuser2@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Unlike Test Post", "Content")
    # Like first
    client.post(f"/posts/{post_id}/like?user_id={user_id}")
    # Then unlike
    response = client.delete(f"/posts/{post_id}/like?user_id={user_id}")
    assert response.status_code == 204

def test_get_post_likes():
    user_id = create_user_and_get_id("likeuser3", "likeuser3@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Get Likes Post", "Content")
    # Like the post
    client.post(f"/posts/{post_id}/like?user_id={user_id}")
    response = client.get(f"/posts/{post_id}/likes")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user_id"] == user_id
    assert data[0]["post_id"] == post_id

def test_like_already_liked_post():
    user_id = create_user_and_get_id("likeuser4", "likeuser4@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Already Liked Post", "Content")
    # Like first time
    client.post(f"/posts/{post_id}/like?user_id={user_id}")
    # Try to like again
    response = client.post(f"/posts/{post_id}/like?user_id={user_id}")
    assert response.status_code == 400

# Comments tests
def test_add_comment():
    user_id = create_user_and_get_id("commentuser1", "commentuser1@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Comment Test Post", "Content")
    response = client.post(f"/posts/{post_id}/comments?user_id={user_id}", json=comment_payload("Great post!"))
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Great post!"
    assert data["user_id"] == user_id
    assert data["post_id"] == post_id

def test_get_post_comments():
    user_id = create_user_and_get_id("commentuser2", "commentuser2@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Get Comments Post", "Content")
    # Add two comments
    client.post(f"/posts/{post_id}/comments?user_id={user_id}", json=comment_payload("Comment 1"))
    client.post(f"/posts/{post_id}/comments?user_id={user_id}", json=comment_payload("Comment 2"))
    response = client.get(f"/posts/{post_id}/comments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_edit_comment():
    user_id = create_user_and_get_id("commentuser3", "commentuser3@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Edit Comment Post", "Content")
    # Add comment
    response = client.post(f"/posts/{post_id}/comments?user_id={user_id}", json=comment_payload("Original comment"))
    comment_id = response.json()["id"]
    print("response:", response.json())
    print("user_id:", user_id, "comment_id:", comment_id)
    # Edit comment as the same user
    response = client.put(f"/posts/comments/{comment_id}?user_id={user_id}", json=comment_payload("Updated comment"))
    print("response:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated comment"

def test_delete_comment():
    user_id = create_user_and_get_id("commentuser4", "commentuser4@example.com", "pass")
    post_id = create_post_and_get_id(user_id, "Delete Comment Post", "Content")
    # Add comment
    response = client.post(f"/posts/{post_id}/comments?user_id={user_id}", json=comment_payload("Delete me"))
    comment_id = response.json()["id"]
    print("user_id:", user_id, "comment_id:", comment_id)
    # Delete comment as the same user
    response = client.delete(f"/posts/comments/{comment_id}?user_id={user_id}")
    assert response.status_code == 204
    # Try to get deleted comment
    response = client.get(f"/posts/{post_id}/comments")
    print("Comments for post:", response.json())
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0 