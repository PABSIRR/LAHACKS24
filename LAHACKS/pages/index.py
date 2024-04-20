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
    with open("README.md", encoding="utf-8") as readme:
        content = readme.read()
    return rx.markdown(content, component_map=styles.markdown_style)
