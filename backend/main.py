from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

class UserResponse(BaseModel):
    text: str

@app.post("/purpose/")
async def create_item(user_response: UserResponse):
    return {"message": "Purpose Processed"}
