"""Welcome to Reflex!."""

# Import all the pages.
from .pages import *
from .auth import *

from .state.base import State
import reflex as rx

# Create the app.
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap", 
        "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;1,100;1,200;1,300;1,400;1,500;1,600;1,700&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&display=swap",
    ],
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
app.add_page(landing,route="/",title="landing")


# Auth Pages
app.add_page(login,route="/login")
app.add_page(signup,route="/signup")

