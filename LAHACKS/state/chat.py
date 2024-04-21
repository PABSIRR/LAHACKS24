import reflex as rx
import asyncio

from .base import State
from LAHACKS.db_model import Post, User

from datetime import datetime
from sqlmodel import select
from pypdf import PdfReader 
import os

class ChatState(State):
    question: str
    
    chat_history: list[tuple[str, str]]
    
    img: list[str]

    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)

            medical_profile = self.extract_text_from_pdf(f"uploaded_files/{file.filename}")
            os.remove(f"uploaded_files/{file.filename}")

    def extract_text_from_pdf(self, file):
        text = ""
        # creating a pdf reader object 
        reader = PdfReader(file) 
        
        for i in range(len(reader.pages)):
            # creating a page object 
            page = reader.pages[i] 
            # extracting text from each page 
            text += page.extract_text()
        return text

    async def answer(self):
        answer = "I don't know!"
        self.chat_history.append((self.question, ""))

        # Clear the question input.
        self.question = ""
        # Yield here to clear the frontend input before continuing.
        yield

        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.1)
            # Add one letter at a time to the output.
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield
        