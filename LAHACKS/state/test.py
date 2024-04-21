import reflex as rx

from .base import State
from LAHACKS.db_model import Post, User, Question

from datetime import datetime
from sqlmodel import select, or_
from pypdf import PdfReader 
import os

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

MAX_QUESTIONS = 10

# load the Google Gemini Model
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

class TestState(State):
    prompts: list[str] = ["Have doubts about your prescription? Get a second opinion! It's possible your physician make have overlooked something",
                     "Verify whether your dosage is correct",
                     "Make certain that the prescription you've received matches the one prescribed by your doctor. Medications that look-alike or sound-alike are sometimes mixed up! (Note: image or name of medicine is required)",
                     "Learn more about your medication, like how to take it and what it does"]
    value: str = prompts[0]
    show_columns = ["Question", "Answer"]
    question: str
    img: list[str]
    context: str
    username: str = ""
    logged_in: bool = False
    prompt: str = ""
    result: str = ""
    loading: bool = False
    filter: str = ""
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)

            self.context = self.extract_text_from_pdf(f"uploaded_files/{file.filename}")
            
            # Won't store user's medical history!
            os.remove(f"uploaded_files/{file.filename}")

    def extract_text_from_pdf(self, file):
        text = ""
        # Creating a pdf reader object 
        reader = PdfReader(file) 
        
        for i in range(len(reader.pages)):
            # Creating a page object 
            page = reader.pages[i] 
            # Extracting text from each page
            text += page.extract_text()
        return text

    def get_model_input(self, context = "", files = [], images = []) -> list:
        '''takes in input features and creates a list to pass into gemini model'''
        model_images = [Image.open(x) for x in images]
        model_files = [self.extract_text_from_pdf(x) for x in files]
        return list(context)+model_files+model_images

    def perscription_feedback_model(self, model_input: list) -> str :
        model_instructions = """You are a tool designed to provide feedback on diagnosis/prescriptions given by doctors 
        Given the information about the patient, their diagnosis, and their prescription, you are to find any 
        abnormalities, inconsistencies, misinformation, etc. that the doctor may have overlooked when given the patient 
        their prescription."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def dose_feedback_model(self, model_input:list) -> str:
        model_instructions = """You are a tool designed to provide feedback on the dosage of prescriptions given by doctors 
        to patients. Given information about the patients medical history, diagnosis, and the drug prescribed provide 
        feedback on possible areas of ocncern within the dosage given to the patient"""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def med_verify_model(self, model_input:list) -> str:
        model_instructions = """ You are a tool designed to verify that prescriptions given by the doctor match the
        prescription recieved by the patient. Sometimes similarly spelled medications are mixed up and lead to the wrong
        medicine in the patient's hand. Given the diagnosis and the picture of the prescription, notify the user if there are 
        any discrepencies in the medication given."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def med_explanation_model(self, model_input:list) -> str:
        model_instructions = """You are a tool designed to help explain complicated prescriptions and dosage instructions
        to patients simply. When given information about any, some, or all of the following information, you are to provide
        an explanation of what the drug is, what it does, and how to administer the drug given the dosage. The information
        you should be able to process is: an image of the drug bottle, description of the general diagnosis/drug name, or 
        the doctors notes given to the patient about the diagnosis and prescription."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def get_result(self, form_data: dict[str, str]):
        self.prompt = self.value
        with rx.session() as session:
            if (
                session.exec(
                    select(Question)
                    .where(Question.username == self.username)
                    .where(Question.prompt == self.prompt)
                ).first()
                or len(
                    session.exec(
                        select(Question)
                        .where(Question.username == self.username)
                        .where(
                            Question.timestamp
                            > datetime.datetime.now() - datetime.timedelta(days=1)
                        )
                    ).all()
                )
                > MAX_QUESTIONS
            ):
                return rx.window_alert(
                    "You have already asked this question or have asked too many questions in the past 24 hours."
                )
        self.result = ""
        self.loading = True
        yield
        try:
            """Respond to prompt"""
            model_inputs = self.get_model_input( prompt = self.question, images = [] )
            if (self.prompt == self.prompts[0]):
                answer = self.perscription_feedback_model(model_inputs)
            elif (self.prompt == self.prompts[1]):
                answer = self.dose_feedback_model(model_inputs)
            elif (self.prompt == self.prompts[2]):
                answer = self.med_verify_model(model_inputs)
            elif (self.prompt == self.prompts[3]):
                answer = self.med_explanation_model(model_inputs)
            self.result = answer
        except Exception as e:
            print(e)
            return rx.window_alert("Error occured with OpenAI execution.")
        finally:
            self.loading = False

    def save_result(self):
        with rx.session() as session:
            answer = Question(
                username=self.username, prompt=self.prompt, answer=self.result
            )
            session.add(answer)
            session.commit()

    @rx.var
    def questions(self) -> list[Question]:
        """Get the users saved questions and answers from the database."""
        with rx.session() as session:
            if self.logged_in:
                query = select(Question).where(Question.username == self.username)
                if self.filter:
                    query = query.where(
                        or_(
                            Question.prompt.ilike(f"%{self.filter}%"),
                            Question.answer.ilike(f"%{self.filter}%"),
                        )
                    )
                return session.exec(
                    query.distinct(Question.prompt)
                    .order_by(Question.timestamp.desc())
                    .limit(MAX_QUESTIONS)
                ).all()
            else:
                return []