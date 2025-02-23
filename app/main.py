from fastapi import FastAPI
from langchain_ai21 import ChatAI21
from pydantic import BaseModel

from app.parser import ExpenseJsonOutputParser, ExpenseParser

app = FastAPI()

json_parser = ExpenseJsonOutputParser()
model = ChatAI21(model="jamba-instruct")
parser = ExpenseParser(model, json_parser)


class UserMessage(BaseModel):
    text: str


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/parse")
async def parse_expense(message: UserMessage):
    return await parser.parse(message.text)
