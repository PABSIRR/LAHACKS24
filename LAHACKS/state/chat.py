import reflex as rx
import asyncio

from .base import State
from LAHACKS.db_model import Post, User

from datetime import datetime
from sqlmodel import select

class ChatState(State):
    question: str
    
    chat_history: list[tuple[str, str]]
    
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
        