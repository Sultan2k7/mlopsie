from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db # type: ignore
from models import Post, User
from schemas import PostCreate, PostRead

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_post = Post(title=post.title, content=post.content, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[PostRead])
def get_posts(skip: int = 0, limit: int = 10, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Post)
    if user_id:
        query = query.filter(Post.user_id == user_id)
    posts = query.offset(skip).limit(limit).all()
    return posts

@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = post.title # type: ignore
    db_post.content = post.content # type: ignore
    db_post.user_id = user_id # type: ignore
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return None

@router.get("/user/{user_id}", response_model=List[PostRead])
def get_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts 