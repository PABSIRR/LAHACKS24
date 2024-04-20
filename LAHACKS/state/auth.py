import reflex as rx
from sqlmodel import select

from .base import State, User

class AuthState(State):
    
    username: str
    password: str
    
    confirm: str
    
    def signup(self):
        with rx.session() as session:
            if self.password != self.confirm:
                return rx.window_alert("Passwords do not match.")
            if session.exec(select(User).where(User.username == self.username)).first():
                return rx.window_alert("Username already exists.")
            self.user = User(username=self.username, password=self.password)
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            print("ok")
            return rx.redirect("/home")
        
    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(
                select(User).where(User.username == self.username)
            ).first()
            if user and user.password == self.password:
                self.user = user
                return rx.redirect("/home")
            else:
                return rx.window_alert("Invalid username or password.")
