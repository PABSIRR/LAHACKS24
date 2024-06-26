import reflex as rx

from LAHACKS.state import base
from LAHACKS import styles

def landing() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    depth_ai_style = {
        "font-family": "IBM Plex Sans Condensed",
        "font-style": "normal",
        "font-weight": "600",
        "font-size": "150px",
        "line-height": "165px",
        "color": "#3B495B",
        "text-shadow": "6px 6px 4px rgba(0, 0, 0, 0.15)",
    }
    return rx.vstack(
        rx.hstack(
            rx.button("About Us", padding_right= 35, padding_left= 35, padding_top= 5, on_click = rx.scroll_to("Section2"),style=styles.button_style_landing),
            rx.button("Chat", padding_top= 5, on_click=rx.redirect("/chat"),style=styles.button_style_landing),
            rx.spacer(),
            rx.text("DEPTH.AI", color = "#3B495B", font_weight= "bold", font_size = "28px"),
            rx.spacer(),
            rx.button("Sign Up", padding_top= 5, on_click=rx.redirect("/login"),style=styles.button_style_landing),
            rx.text(" | ", padding_top= 5),
            rx.button("Log In  ", padding_right=35, padding_top=5, on_click=rx.redirect("/login"),style=styles.button_style_landing),
            width="100%",
            border_bottom="1px solid white",
            padding="0.5em",
            #background_color="#56709B"
        ),
        rx.vstack(
            rx.heading("WELCOME TO", font_family="Lato", font_size=45),
            rx.heading("DEPTH.AI",style=depth_ai_style),
            rx.heading("Your medical care companion", font_style="italic", font_family = "Lato", padding_bottom=10),
            rx.button("Try It Out", font_family="Lato", font_size=25, color="white", width=300, 
                        height=81.0389627229, line_height="175px",border_radius=30, background="#56709B", 
                        on_click=rx.redirect("/chat")),
            width="100%",
            #height="100%",
            align="center",
            justify="center",
            height="100vh",
            id = "Section1"
        ),
        rx.vstack(
            rx.heading("ABOUT US", font_family="Lato", font_size=45, padding_bottom = "50px"),
            #rx.heading("We are a group of passionate college students aiming to make an impact \n in preventing avoidable health care errors. \n Medical errors account for 251,000 deaths in the US and 44% of these errors are mistakes in medicine.", font_style="italic", font_family = "Lato", padding_bottom=10),
            rx.flex(
                rx.card(rx.markdown("We are a group of passionate freshman in college looking to make an impact in reducing medical errors in healthcare and save lives. \n\n Medical errors account for **251,000 deaths** in the US and **44%** of these errors are mistakes in medicine. We aim to reduce these errors \n\n through the use of DEPTH.AI, a medical tool that helps the patient get a second opinion their prescription and diagnoses. "), align="center",font_family="Lato", font_size="24",size="5", color="black"),
                spacing="2",
                align_items="flex-start",
                flex_wrap="wrap",
            ),
            width="100%",
            align="center",
            justify="center",
            height="100vh",
            id = "Section2",
        ),
        align = "center",
        bg="#C6CFDE"
    )
