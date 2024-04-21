"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .auth import *
from .pages import landing

from .state.base import State
import reflex as rx

# Create the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="sky",
        gray_color="mauve",
    )
)

# General Pages
app.add_page(chat,on_load=State.check_login())
app.add_page(index,on_load=State.check_login())
#app.add_page(settings,on_load=State.check_login())
app.add_page(landing,route="/",title="landing")

# Auth Pages
app.add_page(login,route="/login")
app.add_page(signup,route="/signup")

