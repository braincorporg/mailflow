from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    email: str
    project: str
    budget: str

@app.post("/api/submit")
async def create_item(item: Item):
    return {"name": item.name, "email": item.email, "project": item.project, "budget": item.budget}
