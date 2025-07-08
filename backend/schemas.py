from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id: int
    created_at: datetime
    user_id: int

    model_config = {"from_attributes": True}

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    posts: List[PostRead] = []

    model_config = {"from_attributes": True}