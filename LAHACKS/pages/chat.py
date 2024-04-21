from LAHACKS.templates import template
from LAHACKS.state.chat import ChatState
from LAHACKS.db_model import Post, User, Question
from LAHACKS import styles

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
                rx.markdown(ChatState.result),
                rx.cond(
                    ChatState.loading,
                    rx.text("AI is answering...", color_scheme="gray"),
                ),
            ),
            type="hover",
            width="100%",
            max_height="50%",
        ),
        rx.cond(
            ChatState.logged_in & (ChatState.result != ""),
            rx.button("Save Answer", on_click=ChatState.save_result, width="100%"),
        ),
    )


def upload() -> rx.Component:
    color = "rgb(88, 163, 191)"
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button("Select any relevant files (i.e. health documents)", color="black", bg="white", border=f"1px solid {color}",width="100%"),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="2em",
            on_drop=ChatState.handle_upload(rx.upload_files(upload_id="upload1")),
            width="100%"
        ),
        rx.hstack(rx.foreach(rx.selected_files("upload1"), rx.text)),
        # rx.button(
        #     "Upload",
        #     on_click=ChatState.handle_upload(rx.upload_files(upload_id="upload1")),
        # ),
        # rx.button(
        #     "Clear",
        #     on_click=rx.clear_selected_files("upload1"),
        # ),
        rx.foreach(ChatState.img, lambda img: rx.image(src=rx.get_upload_url(img), max_width="10%")),
        padding="4em",
    )

def ask_gpt_form() -> rx.Component:
    return rx.vstack(
        upload(),
        rx.form(
            rx.vstack(
                rx.text_area(placeholder="Provide any other relevant context (optional)",
                             name="context",
                             width="100%",
                             max_height="50%",
                             auto_complete=True),
                rx.select(
                    ChatState.prompts,
                    on_change=ChatState.set_value,
                    color="blue",
                    variant="soft",
                    radius="full",
                    width="100%",
                    size="2",
                    background_color="#C6CFDE"
                ),
                rx.button("Ask", width="100%",background_color="#56709B"),
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
            rx.cond(
                ChatState.loaded,
                rx.vstack(
                    rx.image(src="/logo_actual.svg", height="2em"),
                    rx.heading("What can we answer today?", font_size="1.5em", align="center",padding_bottom="0.5em"),
                    width="100%",
                    align="center"
                ),
            ),
            rx.card(ask_gpt_form(),width="100%"),
            rx.cond(
                ChatState.logged_in,
                rx.card(saved_qa(),width="100%"),
            ),
            spacing="4",
            width="100%",
            margin_left="auto",
            flex_wrap="wrap",
            flex_basis="100%"
        ),
        justify="center",
        padding_top="1em",
        text_align="top",
        position="relative",
        width="100%",
        margin_left="auto",
        flex_wrap="wrap",
        flex_basis="100%"
        
    )