import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from sqlalchemy.orm import Session
from backend.database import engine, Base, SessionLocal
from backend.models import User, Post
from sqlalchemy.exc import IntegrityError

# Create tables
Base.metadata.create_all(bind=engine)

def create_dummy_data():
    db: Session = SessionLocal()
    try:
        # Create users
        user1 = User(username="alice", email="alice@example.com", hashed_password="fakehashed1")
        user2 = User(username="bob", email="bob@example.com", hashed_password="fakehashed2")
        db.add_all([user1, user2])
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        # Create posts
        post1 = Post(title="Hello World", content="This is Alice's first post!", user_id=user1.id)
        post2 = Post(title="Bob's Thoughts", content="Bob shares his thoughts.", user_id=user2.id)
        db.add_all([post1, post2])
        db.commit()
        print("Dummy data inserted successfully.")
    except IntegrityError:
        db.rollback()
        print("Dummy data already exists or integrity error.")
    finally:
        db.close()

if __name__ == "__main__":
    create_dummy_data() 