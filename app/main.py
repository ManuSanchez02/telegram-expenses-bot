import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.concurrency import asynccontextmanager
from langchain_ai21 import ChatAI21
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Database
from app.models.expense import Expense
from app.parser import ExpenseJsonOutputParser, ExpenseParser
from app.schemas import UserMessage

load_dotenv()

json_parser = ExpenseJsonOutputParser()
model = ChatAI21(model="jamba-instruct")
parser = ExpenseParser(model, json_parser)


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"


db = Database()

SessionDep = Annotated[AsyncSession, Depends(db.get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.initialize(POSTGRES_URL)
    yield
    db.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.post("/parse")
async def parse_expense(message: UserMessage, session: SessionDep):
    res = await parser.parse(message.text)
    expense = Expense(
        user_id=1,
        description=res["description"],
        amount=res["price"],
        category=res["category"],
    )
    session.add(expense)
    await session.commit()
    return f"{res['category']} expense added ✅"
