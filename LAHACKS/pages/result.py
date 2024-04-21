from LAHACKS import styles
from LAHACKS.templates import template
from LAHACKS.state import home
from LAHACKS.state.chat import ChatState

import reflex as rx

@template(route="/result", title="Result")
def result() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Welcome to Reflex! Create a chat to get started."),
    )