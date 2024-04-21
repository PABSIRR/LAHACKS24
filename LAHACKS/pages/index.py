"""The home page of the app."""

from LAHACKS import styles
from LAHACKS.templates import template
from LAHACKS.state import home

import reflex as rx

@template(route="/home", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Welcome to Reflex!"),
    )