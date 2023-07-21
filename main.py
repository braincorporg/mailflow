# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 17:23:58 2023

@author: Kevin Lopez
"""

from fastapi import FastAPI
from pydantic import BaseModel
from google_sheets import write_to_sheet # This is a hypothetical module, you will need to create it based on the Google Sheets API guide.

app = FastAPI()

class Item(BaseModel):
    name: str
    email: str
    project: str
    budget: str

@app.post("/api/submit")
async def create_item(item: Item):
    write_to_sheet(item.name, item.email, item.project, item.budget)
    return item
