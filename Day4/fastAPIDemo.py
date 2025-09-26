from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Hello FastAPI"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}


class EchoRequest(BaseModel):
    text: str
    title: str | None = None

@app.post("/echo")
async def echo(request: EchoRequest):
    # Returns the same JSON sent
    # return {"data": request, "message": "This is your echoed text"}
    return request