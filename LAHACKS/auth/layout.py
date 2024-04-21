import reflex as rx

def container(*children, **props):
    """
        Define some props that should be the same for both login/signup
    """
    props = (
        dict(
            width="30%",
            background="white",
            height="100%",
            px="9",
            margin="0 auto",
            position="relative",
            border_radius="40px",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            padding_top="50px",
            padding_bottom="24px",
            spacing="4",
        )
        | props
    )
    return rx.stack(*children, **props)

def auth_layout(*args):
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading("DEPTH.AI",font_family="IBM Plex Sans Condensed",padding_bottom="125px",on_click=rx.redirect("/")),
                rx.image(src="/logo_actual.svg", height="2em"),
                top="2em",
                left="2em",
                position="sticky",
                size=5
            ),
        ),
            container(
                rx.vstack(
                    rx.heading("Sign Up",font_family="Lato",font_weight="400",size="8"),
                    rx.heading("Your Digital Care Companion",size="2"),
                    align="center",
                ),
                *args, 
            )
        )