import reflex as rx
from sqlmodel import select
import regex as re
from .base import State, User

class AuthState(State):
    
    username: str
    password: str
    email: str
    
    confirm: str
    
    def signup(self):
        with rx.session() as session:
            pattern = re.compile(r'^(?=.*[a-z]|[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}|:<>?/~`])[A-Za-z\d!@#$%^&*()_+{}|:<>?/~`]{8,}$')
            pattern2 = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
            if self.password != self.confirm:
                return rx.window_alert("Passwords do not match.")
            if session.exec(select(User).where(User.username == self.username)).first():
                return rx.window_alert("Username already exists.")
            if not bool(pattern.match(self.password)):
                return rx.window_alert("Password must\ncontain a digit and special character\nbe at least 8 characters long")
            if not bool(pattern2.match(self.email)):
                return rx.window_alert("Invalid Email")
            self.user = User(username=self.username, password=self.password, email=self.email)
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
                return rx.redirect("/chat")
            else:
                return rx.window_alert("Invalid username or password.")
