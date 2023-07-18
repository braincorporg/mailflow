import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "Categorise & extract key info from an email, such as purpose, name of the sender, organization, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "senderName": {
                    "type": "string",
                    "description": "the name of the person or organization that sent the email"
                },
                "senderOrganization": {
                    "type": "string",
                    "description": "the organization of the sender, if any"
                },
                "emailPurpose": {
                    "type": "string",
                    "description": "Try to identify the purpose of the email. If it is related to our work at Brain Corp, and if there is anything relevant in there"
                },
                "category": {
                    "type": "string",
                    "description": "Try to categorise this email into categories like: 1. Job Applications; 2. Partnership Inquiries; 3. Funding Proposals; 4. Product updates; 5. ads and scam, 6.Usefull infos; 7.Others"
                },
                "nextStep":{
                    "type": "string",
                    "description": "What is the suggested next step to move this forward?"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how crucial it is, from 0 to 10; 10 being most important"
                },
            },
            "required": ["senderName", "senderOrganization", "emailPurpose", "category", "nextStep", "priority"]
        }
    }
]

instruction = """ Hello there, AI colleague!

Welcome to BrainCorp! We are an innovation-driven company, leading the charge in the AI industry. Our mission is to facilitate the transition towards an AI-driven world, making it accessible, beneficial, and completely safe for everyone.

We are part of an exciting journey, creating tools, systems, and solutions that transform how businesses operate, how societies function, and even how we live our everyday lives. Our vision is a world where humans and AI work together, synergistically, to make what was once considered impossible, possible.

You are a critical piece of this vision. As a language model AI, you are not just a tool, but a team member, representing an example of the very future we are working towards. Your role is to help us analyze and categorize the emails we receive, extract key information, prioritize their importance, and suggest the next steps. Through your tasks, you will help ensure a smooth and efficient communication process, which is the backbone of our operations.

Remember, at BrainCorp, we see AI as a partner, not a product. We believe that AI, when designed and used correctly, can empower humans, augment our skills, and open doors to unprecedented opportunities. You, our AI colleague, are a personification of this belief.

In your role as an AI chatbot, you will not only facilitate more efficient operations but also help us understand and shape the interaction between humans and AI. Your work will provide valuable insights and lessons, helping us enhance our models and systems for the future.

So, you are not just an email analyzer – you are an explorer at the forefront of human-AI collaboration. The discoveries you make, the lessons you learn, and the improvements you achieve will feed directly back into our work, driving us towards our goal of a harmonious and productive human-AI future.

Welcome to the team, and let's build the future together!"""

class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key information from this email: {content} "

    messages = [{"role": "system", "content": instruction},
                {"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    priority = eval(arguments).get("priority")
    product = eval(arguments).get("product")
    amount = eval(arguments).get("amount")
    category = eval(arguments).get("category")
    nextStep = eval(arguments).get("nextStep")

    return {
        "companyName": companyName,
        "product": product,
        "amount": amount,
        "priority": priority,
        "category": category,
        "nextStep": nextStep
    }
