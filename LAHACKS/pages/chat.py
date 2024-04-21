from LAHACKS.templates import template
from LAHACKS.state.chat import ChatState
from LAHACKS.db_model import Post, User, Question

import reflex as rx

MAX_QUESTIONS = 100

def result_view() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.cond(
                ChatState.loading,
                rx.chakra.spinner(),
            ),
            justify="between",
        ),
        rx.scroll_area(
            rx.cond(
                ChatState.result,
                rx.text(ChatState.result),
                rx.cond(
                    ChatState.loading,
                    rx.text("AI is answering...", color_scheme="gray"),
                    rx.text(
                        "Ask a question to get an answer from GPT.", color_scheme="gray"
                    ),
                ),
            ),
            type="hover",
            width="100%",
            max_height="7em",
        ),
        rx.cond(
            ChatState.logged_in & (ChatState.result != ""),
            rx.button("Save Answer", on_click=ChatState.save_result, width="100%"),
        ),
    )


def upload() -> rx.Component:
    color = "rgb(107,99,246)"
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button("Select any relevant files (i.e. health documents)", color=color, bg="white", border=f"1px solid {color}"),
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

def ask_gpt_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Ask DEPTH.AI", font_size="1.5em", align="center"),
        upload(),
        rx.form(
            rx.vstack(
                rx.input(placeholder="Provide any other relevant context (optional)", name="context", width="100%"),
                rx.select(
                    ChatState.prompts,
                    on_change=ChatState.set_value,
                    color="blue",
                    variant="soft",
                    radius="full",
                    width="100%",
                ),
                rx.button("Ask", width="100%"),
                spacing="3",
            ),
            on_submit=ChatState.get_result,
            reset_on_submit=True,
        ),
        rx.divider(),
        result_view(),
        align="stretch",
        spacing="3",
        width="100%",
    )


def saved_qa_item(qa: Question, ix: int) -> rx.Component:
    return rx.accordion.item(
        header=rx.text(qa.prompt, size="3", align="left"),
        content=rx.scroll_area(
            rx.text(qa.answer, size="2"),
            type="hover",
            max_height="10em",
            padding="12px",
        ),
        value=f"item-{ix}",
    )


def saved_qa() -> rx.Component:
    return rx.vstack(
        rx.heading("Saved Q&A", font_size="1.5em"),
        rx.divider(),
        rx.input(
            placeholder="Filter",
            value=ChatState.filter,
            on_change=ChatState.set_filter,
            debounce_timeout=1500,
            width="100%",
        ),
        rx.accordion.root(
            rx.foreach(
                ChatState.questions,
                saved_qa_item,
            ),
            single=False,
            collapsible=True,
        ),
        spacing="3",
        padding="1em",
        width="100%",
    )

@template(route="/chat", title="Chat")
def chat() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.card(ask_gpt_form()),
            rx.cond(
                ChatState.logged_in,
                rx.card(saved_qa()),
            ),
            spacing="4",
            width="100%",
        ),
        justify="center",
        padding_top="6em",
        text_align="top",
        position="relative",
        width="100%"
    )