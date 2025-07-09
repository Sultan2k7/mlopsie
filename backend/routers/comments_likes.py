from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db # type: ignore
from models import Post, User, Like, Comment
from schemas import LikeRead, CommentCreate, CommentRead

router = APIRouter(prefix="/posts", tags=["Likes & Comments"])

# Likes endpoints
@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED, response_model=LikeRead)
def like_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not post or not user:
        raise HTTPException(status_code=404, detail="User or Post not found")
    existing = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already liked")
    like = Like(user_id=user_id, post_id=post_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

@router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    like = db.query(Like).filter(Like.user_id == user_id, Like.post_id == post_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(like)
    db.commit()
    return None

@router.get("/{post_id}/likes", response_model=List[LikeRead])
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    likes = db.query(Like).filter(Like.post_id == post_id).all()
    return likes

# Comments endpoints
@router.post("/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def add_comment(post_id: int, comment: CommentCreate, user_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not post or not user:
        raise HTTPException(status_code=404, detail="User or Post not found")
    new_comment = Comment(post_id=post_id, user_id=user_id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}/comments", response_model=List[CommentRead])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@router.put("/comments/{comment_id}", response_model=CommentRead)
def edit_comment(comment_id: int, comment: CommentCreate, user_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not owned by user")
    db_comment.content = comment.content # type: ignore
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == user_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found or not owned by user")
    db.delete(db_comment)
    db.commit()
    return None 