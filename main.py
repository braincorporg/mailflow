from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://braincorp.fr",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AIRTABLE_API_KEY = os.getenv("AIRTABLE_TOKEN")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("TABLE_ID")

def write_to_airtable(name, email, project, budget):
    headers = {
        'Authorization': f'Bearer {AIRTABLE_API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "Email": email,
                    "project": project,
                    "budget": budget
                }
            }
        ]
    }

    response = requests.post(
        f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code

class Item(BaseModel):
    name: str
    email: str
    project: str
    budget: str

@app.post("/api/submit")
async def create_item(item: Item):
    response = write_to_airtable(item.name, item.email, item.project, item.budget)
    return response
