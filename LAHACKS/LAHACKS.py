"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .auth import login, signup
from .pages import landing

from .state.base import State
import reflex as rx

# Create the app.
app = rx.App()

# General Pages
app.add_page(chat,on_load=State.check_login())
app.add_page(index,on_load=State.check_login())
app.add_page(settings,on_load=State.check_login())
app.add_page(landing.landing(),route="/",title="landing")

# Auth Pages
app.add_page(login.login(),route="/login")
app.add_page(signup.signup(),route="/signup")

