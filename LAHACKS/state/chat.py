import reflex as rx
import asyncio

from .base import State
from LAHACKS.db_model import Post, User

from datetime import datetime
from sqlmodel import select
from pypdf import PdfReader 
import os

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

# load the Google Gemini Model
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")

class ChatState(State):
    question: str
    
    chat_history: list[tuple[str, str]]
    
    img: list[str]

    medical_profile: str
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)

            self.medical_profile = self.extract_text_from_pdf(f"uploaded_files/{file.filename}")
            
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

    def get_model_input(self, prompt = "", files = [], images = []) -> list:
        '''takes in input features and creates a singular prompt list to pass into gemini model'''
        model_images = [Image.open(x) for x in images]
        model_files = [self.extract_text_from_pdf(x) for x in files]
        return list(prompt)+model_files+model_images

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
        an explanation of what the drug is, what it does, and how to administer the drug given the dosage . The information
        you should be able to process is: an image of the drug bottle, description of the general diagnosis/drug name, or 
        the doctors notes given to the patient about the diagnosis and prescription."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    async def answer(self):
        # context = """A 69-year-old man with a history of cervical stenosis, coronary artery disease, chronic 
        # kidney disease, and hypertension developed worsening neck pain in the previous year, which prevented him from 
        # working, performing household tasks, and socializing with friends. Due to severe osteoarthritis and pain in his 
        # nees, he used a motorized scooter. The patient was admitted for elective surgery for decompression and to extend a 
        # prior C3-C6 fusion down to T3. Surgery was performed which concluded at approximately 13:00. The patient recovered 
        # in the post-anesthesia care unit (PACU), where he was placed on hydromorphone patient-controlled analgesia (PCA) for 
        # pain control and also received his usual home doses of gabapentin and acetaminophen."""
        model_inputs = self.get_model_input( prompt = self.question, images = [] )
        answer = self.perscription_feedback_model(model_inputs)
        self.chat_history.append((self.question, answer))

        # Clear the question input.
        self.question = ""
        # Yield here to clear the frontend input before continuing.
        yield

        for i in range(len(answer)):
            # Pause to show the streaming effect.
            await asyncio.sleep(0.01)
            # Add one letter at a time to the output.
            self.chat_history[-1] = (
                self.chat_history[-1][0],
                answer[: i + 1],
            )
            yield
        