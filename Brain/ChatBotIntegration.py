""" At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai """

import google.generativeai as genai 
from os import environ 
from dotenv import load_dotenv

load_dotenv() 
API = environ['GIMINE_API']

genai.configure(api_key=API)

#Set up the model
generation_config = { "temperature": 1, "top_p": 0.95, "top_k": 64, "max_output_tokens": 8192, }

safety_settings = [ { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE" }, 
                { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE" }, 
                { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE" },
                { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE" }, ]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

convo = model.start_chat(history=[ ])

def ask_ai(question):
     try:
         convo.send_message(f"{question} ,always answer in short and sweet")
         return convo.last.text 
     except Exception as e: 
        print(f"An error occurred while communicating with the AI: {e}") 
        return None