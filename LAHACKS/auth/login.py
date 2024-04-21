import reflex as rx

from LAHACKS.auth.layout import auth_layout
from LAHACKS.state.auth import AuthState

def login():
    """The login page."""
    return auth_layout(
        rx.box(
            rx.vstack(
                rx.box(
                    rx.input(
                        placeholder="Username",
                        on_blur=AuthState.set_username,
                        size="3",
                        width="100%",
                    ),
                    width="100%"
                ),
                rx.box(
                    rx.input(
                        type="email",
                        placeholder="Email",
                        on_blur=AuthState.set_email,
                        size="3",
                        width="100%",
                    ),
                    width="100%"
                ),
                rx.box(
                    rx.input(
                        type="password",
                        placeholder="Password",
                        on_blur=AuthState.set_password,
                        size="3",
                        width="100%",
                    ),
                    width="100%"
                ),
                rx.button("Log in", on_click=AuthState.login, size="3", width="100%",border_radius="2px",background="#98ADCF",
                color="white"),
                spacing="4",
                flex_direction="column",
                width="100%"
            ),
            align_items="left",
            background="white",
            border="1px solid #eaeaea",
            padding="16px",
            width="400px",
            border_radius="8px",
        ),
        rx.text(
            "New to DEPTH.AI ",
            rx.link("Sign up here.", href="/signup",color="#56709B"),
            color="black",
            align="center"
        ),
    )

