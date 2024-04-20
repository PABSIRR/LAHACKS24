"""The home page of the app."""

from LAHACKS import styles
from LAHACKS.templates import template
from LAHACKS.state import home

import reflex as rx
import os
import pathlib
import tqdm
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@template(route="/home", title="Home")
def index() -> rx.Component:
    """The home page.

    Returns:
        The UI for the home page.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content("Write a story about a magic backpack.")
    
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.text("Welcome to Reflex!"),
        rx.text(response.text),
    )

def convert_pdf_to_text():
    pass

def check_dosage():
    pass