import reflex as rx

def container(*children, **props):
    """
        Define some props that should be the same for both login/signup
    """
    props = (
        dict(
            width="100%",
            max_width="960px",
            background="white",
            height="100%",
            px="9",
            margin="0 auto",
            position="relative",
            border_top_radius="10px",
            box_shadow="0 4px 60px 0 rgba(0, 0, 0, 0.08), 0 4px 16px 0 rgba(0, 0, 0, 0.08)",
            display="flex",
            flex_direction="column",
            align_items="center",
            padding_top="36px",
            padding_bottom="24px",
            spacing="4",
        )
        | props
    )
    return rx.stack(*children, **props)

def auth_layout(*args):
    return rx.box(
        container(
            rx.vstack(
                rx.heading("Depth"),
                rx.heading("Sign in or create an account"),
                align="center"
            ),
            *args, 
        )
    )
    