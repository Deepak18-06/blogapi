from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(...)

class UserInDB(BaseModel):
    username: str = Field(..., max_length=50)
    hashed_password: str

class BlogPost(BaseModel):
    title: str = Field(..., max_length=100)
    content: str
    author: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class BlogPostInDB(BlogPost):
    id: str
