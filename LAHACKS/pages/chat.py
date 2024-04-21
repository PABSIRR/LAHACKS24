"""The chat page."""

from LAHACKS.templates import template
from LAHACKS.state.chat import ChatState
from LAHACKS import styles

import reflex as rx


def chat_func() -> rx.Component:
    return rx.box(
        rx.foreach(
            ChatState.chat_history,
            lambda messages: qa(messages[0], messages[1])
        )
    )
    
def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(question, text_align="right",style=styles.question_style),
        rx.box(answer, text_align="left",style=styles.answer_style),
        margin_y="1em",
    )
    
def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value=ChatState.question,
            placeholder="Ask a question",
            on_change=ChatState.set_question,
            style=styles.input_style,
        ),
        rx.button(
            "Ask",
            on_click=ChatState.answer,
            style=styles.button_style,
        ),
    )

def upload_btn() -> rx.Component:
    color = "rgb(107,99,246)"
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button("Select File", color=color, bg="white", border=f"1px solid {color}"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),
        rx.button(
            "Upload",
            on_click=ChatState.handle_upload(rx.upload_files(upload_id="upload1")),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(ChatState.img, lambda img: rx.image(src=rx.get_upload_url(img))),
        padding="5em",
    )

@template(route="/chat", title="Chat")
def chat() -> rx.Component:
    return rx.center(
        rx.vstack(
            chat_func(),
            action_bar(),
            upload_btn(),
            align="center",
        ),
        width="100%",
        display="flex",
        border="black",
    )
"""
@template(route="/chat", title="Chat")
def chat() -> rx.Component:
    return(
        rx.heading("ID DO IT")
    )
"""

