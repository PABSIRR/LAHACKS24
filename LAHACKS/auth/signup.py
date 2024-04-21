import reflex as rx

from LAHACKS.auth.layout import auth_layout
from LAHACKS.state.auth import AuthState

def signup():
    """The sign up page."""
    return auth_layout(
        rx.box(
            rx.vstack(
                rx.box(
                    rx.input(
                        placeholder="Username",
                        on_blur=AuthState.set_username,
                        size="3",
                        width="100%"
                    ),
                    width="100%"
                ),
                rx.box(
                    rx.input(
                        placeholder="Email",
                        type="email",
                        on_blur=AuthState.set_email,
                        size="3",
                        width="100%"
                    ),
                    width="100%"
                ),
                rx.box(
                    rx.input(
                    type="password",
                    placeholder="Password",
                    on_blur=AuthState.set_password,
                    size="3",
                    width="100%"
                    ),
                    width="100%"    
                ),
                rx.box(
                    rx.input(
                    type="password",
                    placeholder="Confirm password",
                    on_blur=AuthState.set_confirm,
                    size="3",
                    width="100%"
                    ),
                    width="100%"    
                ),
                rx.box(
                    rx.button(
                        "Sign up",
                        on_click=AuthState.signup,
                        size="3",
                        width="100%",
                        border_radius="4px"
                    ),
                    width="100%"
                ),
                spacing="4",
            ),
            align_items="left",
            background="white",
            border="1px solid #eaeaea",
            padding="16px",
            width="400px",
            border_radius="8px",
        ),
        rx.text(
            "Already have an account? ",
            rx.link("Sign in here.", href="/login"),
            color="gray",
        ),
    )
