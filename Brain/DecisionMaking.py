URL = 'https://kaushikshresth12-kaushikbhaiyakaserver.hf.space/generate-text'
from time import sleep
from rich import print
from os import environ
from dotenv import load_dotenv
import requests

load_dotenv()
API = environ['HF_TOKEN']


def format_prompt(message, custom_instructions=None):
    prompt = ""
    if custom_instructions:
        prompt += f"[INST] {custom_instructions} [/INST]"
    prompt += f"[INST] {message} [/INST]"
    return prompt


instructions_L1 = """
You are Decision Making Model.
which select 2 options give below:
-> 'Query' if the input is a question that chatbot should answer.
-> 'Automation' if the input is an instruction to open or close anything in computer. Generate any image, open any website, open any app, open any file, open any folder, open any file, open any folder, cloase any file, close any folder, close any app, close any website, close any image, close any file, close any folder, close computer, search anything, play any song, play any video etc. (whatever task that chat bot can perform)
***The output should be only one word***
Example (1) : hello can you open chrome for me?
Example Output (1) : Automation
Example (2) : Search Akshya kumar on Wikipedia?
Example Output (2) : Automation
Example (3) : who is akshay kumar?
Example Output (3) : Query
Example (4) : play music on youtube?
Example Output (4) : Automation
Example (5) : well, play music on youtube?
Example Output (5) : Automation
Example (6) : No, i think he is human being.
Example Output (6) : Query
Example (7) : i mean to say can you open chrome?
Example Output (7) : Automation
Example (8) : okay tell me a joke+
Example Output (8) : Query
"""

template_L1 = """#reply only one of them ["Automation", "Query"]
Input : *{prompt}*
Output : 
"""

instructions_L2 = """Today is 15/03/2024.
You are Decision Making Model.
which select 2 options give below:
-> 'Before' if the information is before 07/02/2023. if the information is about who was or any past event. or any chat bot response. like anything which a chat bot can answer without knowing current events. 
-> 'After' if the information is after 07/02/2023. if the information is about who will be or any future event. or any present event. time, date, month, year, recent event or any event. for present and future event. if the question is about any person. example: who is Kaushik Shresth? or any other person.
***The output should be only one word***
Example (1) : who was akbar?
Example Output (1) : Before
Example (2) : who is currently working as ceo of microsoft?
Example Output (2) : After
Example (3) : how are you
Example Output (3) : Before
Example (4) : do you know quantum computing?
Example Output (4) : Before"""

template_L2 = """#reply only one of them ["After", "Before"]
Input : *{prompt}*
Output : 
"""

# Create a session
rq = requests.Session()


def Mixtral7B(prompt, instructions, temperature=0.1, max_new_token=2, top_p=0.95, repition_penalty=1.0):
    data = {'prompt': prompt,
            'instructions': instructions,
            'api_key': API}

    response = rq.post(URL, json=data)
    res = response.json()['response']
    return res


def L1(prompt):
    global template_L1
    response: str = Mixtral7B(template_L1.format(prompt=prompt),
                              instructions=instructions_L1)
    return response.strip()


def L2(prompt):
    global template_L2
    response: str = Mixtral7B(template_L2.format(prompt=prompt),
                              instructions=instructions_L2)
    return response.strip()


print(L1("pls open youtube"))
