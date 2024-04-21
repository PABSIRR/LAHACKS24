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

    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("How to Use the Chat"),
        rx.flex(
            rx.card(rx.markdown("**Prescription Feedback** \n\n Based on diagnosis and/or medical records, identify potential mistakes with the prescription given \n\n **Recommended Information to Input:** medical records, doctor’s notes, doctor’s diagnosis."), size="5", color="black"),
            rx.card(rx.markdown("**Prescription Verification** \n\n Based on diagnosis and prescription given, verify the medicine received is actually what the doctor prescribed. \n\n **Recommended Information to Input:** medical records, doctor’s notes, doctor’s prescription, image of medicine received."), size="5", color="black"),
            rx.card(rx.markdown("**Dosage Feedback** \n\n Based on diagnosis and/or medical records, provide feedback on the dosage amount. \n\n **Recommended Information to Input:** medical records, doctor’s notes, doctor’s diagnosis"), size="5", color="black"),
            rx.card(rx.markdown("**Explain My Medication** \n\n Based on diagnosis and/or medical records, prescription and dosage amount, explain what the medicine does simply and how to take it. \n\n **Recommended Information to Input:** medical records, doctor’s notes, doctor’s diagnosis, image of medicine received."), size="5", color="black"),
            spacing="2",
            align_items="flex-start",
            flex_wrap="wrap",
        )
    ),