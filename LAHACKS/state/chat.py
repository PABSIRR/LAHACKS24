import reflex as rx

from .base import State
from LAHACKS.db_model import Post, User, Question

from datetime import timedelta, datetime
from sqlmodel import select, or_
from pypdf import PdfReader 
import os

import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

MAX_QUESTIONS = 100

# load the Google Gemini Model
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
# generation_config = {
#   "temperature": 0.5,
#   "top_p": 0.95,
#   "top_k": 0,
#   "max_output_tokens": 8192,
# }

class ChatState(State):
    show_columns = ["Question", "Answer"]
    prompts: list[str] = ["Concerned about your prescription? Get a second opinion!",
                        "Verify whether your dosage is correct",
                        "Ensure your prescription is correct (image or name needed)",
                        "Explore your medication, its usage, and effects"]
    value: str = prompts[0]     # selected option from dropdown menu; default is first prompt option
    prompt: str = ""
    result: str = ""            # response from Google Gemini based on prompt + context
    pdf_paths: list[str]        # paths of PDFs that are uploaded
    image_paths: list[str]      # paths of images that are uploaded
    img: list[str]              # for file upload functionality

    username: str = ""
    logged_in: bool = False
    loading: bool = False
    filter: str = ""
    
    async def handle_upload(self, files: list[rx.UploadFile]):
        # Files that are upload can be PDFs and/or Images
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)
            print(file.filename)
            # Add file path to appropriate folder so that it can be processed as model inputs
            if (file.filename[-3:].lower() == "pdf"):
                self.pdf_paths.append(f"uploaded_files/{file.filename}")
            else:
                # Assume that file is an image
                self.image_paths.append(f"uploaded_files/{file.filename}")

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

    def get_model_input(self, context = "", pdfs = [], images = []) -> list:
        '''takes in input features and creates a list to pass into gemini model'''
        model_images = [Image.open(x) for x in images]
        model_pdfs = [self.extract_text_from_pdf(x) for x in pdfs]
        # Remove files from local directory; patient data is NOT stored
        for image_path in images: os.remove(image_path)
        for pdf_path in pdfs: os.remove(pdf_path)
        return list(context)+model_pdfs+model_images

    def perscription_feedback_model(self, model_input: list) -> str :
        model_instructions = """You are a tool designed to provide feedback on diagnosis/prescriptions given by doctors 
        Given the information about the patient, their diagnosis, and their prescription, you are to find any 
        abnormalities, inconsistencies, misinformation, etc. that the doctor may have overlooked when given the patient 
        their prescription."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", 
                                  system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def dose_feedback_model(self, model_input:list) -> str:
        model_instructions = """You are a tool designed to provide feedback on the dosage of prescriptions given by doctors 
        to patients. Given information about the patients medical history, diagnosis, and the drug prescribed provide 
        feedback on possible areas of concern within the dosage given to the patient. Make sure to double check normal
        dosage amounts for other patients with similar physical traits, conditions, etc. to validate the dosage amount
        given by the doctor."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", 
                                  system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def med_verify_model(self, model_input:list) -> str:
        model_instructions = """You are a tool designed to verify that prescriptions given by the doctor match the
        prescription recieved by the patient. Sometimes similarly spelled medications are mixed up and lead to the wrong
        medicine in the patient's hand. Given the diagnosis and the picture of the prescription, notify the user if there are 
        any discrepencies in the medication given."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", 
                                  system_instruction=model_instructions)
        response = model.generate_content(model_input)
        return response.text

    def med_explanation_model(self, model_input:list) -> str:
        model_instructions = """You are a tool designed to help explain complicated prescriptions and dosage instructions
        to patients simply. When given information about any, some, or all of the following information, you are to provide
        an explanation of what the drug is, what it does, and how to administer the drug given the dosage . The information
        you should be able to process is: an image of the drug bottle, description of the general diagnosis/drug name, or 
        the doctors notes given to the patient about the diagnosis and prescription."""
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest", 
                                  system_instruction=model_instructions)
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
                            > datetime.now() - timedelta(days=1)
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
            print("context: ", form_data["context"], "\n", "pdfs: ", self.pdf_paths, "\n", "imgs: ", self.image_paths)
            
            model_inputs = self.get_model_input( context=form_data["context"], pdfs=self.pdf_paths, images=self.image_paths )
            if (self.prompt == self.prompts[0]):
                self.result = self.perscription_feedback_model(model_inputs)
            elif (self.prompt == self.prompts[1]):
                self.result = self.dose_feedback_model(model_inputs)
            elif (self.prompt == self.prompts[2]):
                self.result = self.med_verify_model(model_inputs)
            elif (self.prompt == self.prompts[3]):
                self.result = self.med_explanation_model(model_inputs)
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