from sqlmodel import Field
import reflex as rx


class User(rx.Model, table=True):
    """
    Each use has a username / password
    """
    username: str
    password: str
    
class Post(rx.Model, table=True):
    """
    Each post should have like_count, responses?, text
    """
    
    content: str
    like_count: int
    author: str
    created_at: str

"""
class Join(rx.Model, table=True):
    
    followed_username: str = Field(primary_key=True)
    follower_username: str = Field(primary_key=True)
"""