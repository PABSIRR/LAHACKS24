from sqlmodel import Field
import reflex as rx
import datetime

class User(rx.Model, table=True):
    """
    Each user has a username / password
    """
    username: str
    password: str
    email: str
    
class Post(rx.Model, table=True):
    """
    Each post should have like_count, responses?, text
    """
    
    content: str
    like_count: int
    author: str
    created_at: str

class Question(rx.Model, table=True):
    """A table for questions and answers in the database."""
    username: str
    prompt: str
    answer: str
    timestamp: datetime.datetime = datetime.datetime.now()
"""
class Join(rx.Model, table=True):
    
    followed_username: str = Field(primary_key=True)
    follower_username: str = Field(primary_key=True)
"""