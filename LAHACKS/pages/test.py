
from LAHACKS.templates import template
from LAHACKS.state.test import TestState
from LAHACKS.db_model import Post, User, Question

import reflex as rx

MAX_QUESTIONS = 10

def result_view() -> rx.Component:
    return rx.fragment(
        rx.flex(
            rx.text(TestState.prompt),
            rx.cond(
                TestState.loading,
                rx.chakra.spinner(),
            ),
            justify="between",
        ),
        rx.scroll_area(
            rx.cond(
                TestState.result,
                rx.text(TestState.result),
                rx.cond(
                    TestState.loading,
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
            TestState.logged_in & (TestState.result != ""),
            rx.button("Save Answer", on_click=TestState.save_result, width="100%"),
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
            on_click=TestState.handle_upload(rx.upload_files(upload_id="upload1")),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(TestState.img, lambda img: rx.image(src=rx.get_upload_url(img))),
        padding="5em",
    )

def ask_gpt_form() -> rx.Component:
    return rx.vstack(
        rx.heading("Ask DEPTH.AI", font_size="1.5em", align="center"),
        rx.form(
            rx.vstack(
                rx.input(placeholder="Provide any other relevant context (optional)", name="prompt", width="100%"),
                rx.select(
                    TestState.prompts,
                    on_change=TestState.set_value,
                    color="blue",
                    variant="soft",
                    radius="full",
                    width="100%",
                ),
                rx.button("Ask", width="100%"),
                spacing="3",
            ),
            on_submit=TestState.get_result,
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
            value=TestState.filter,
            on_change=TestState.set_filter,
            debounce_timeout=1500,
            width="100%",
        ),
        rx.accordion.root(
            rx.foreach(
                TestState.questions,
                saved_qa_item,
            ),
            single=False,
            collapsible=True,
        ),
        spacing="3",
        padding="1em",
        width="100%",
    )

@template(route="/test", title="Test")
def test() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.card(ask_gpt_form()),
            rx.cond(
                TestState.logged_in,
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