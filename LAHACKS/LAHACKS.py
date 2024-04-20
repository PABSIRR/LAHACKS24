"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .auth import login, signup

from .state.base import State
import reflex as rx

# Create the app.
app = rx.App()

# General Pages
app.add_page(dashboard, on_load=State.check_login())
app.add_page(index)
app.add_page(settings)

# Auth Pages
app.add_page(login.login(),route="/login")
app.add_page(signup.signup(),route="/signup")

