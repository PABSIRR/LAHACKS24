import reflex as rx

from LAHACKS.state import base
from LAHACKS import styles

def landing() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    return rx.vstack(
        rx.heading("DEPTH"),
        rx.heading("Discover More"),
        rx.button("Sign Up",on_click=rx.redirect("/login"))
    )
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)