import logging
import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.concurrency import asynccontextmanager
from langchain_ai21 import ChatAI21
from sqlalchemy import select

from app.auth import validate_api_key
from app.database import SessionDep, db
from app.models import ApiKey, Expense, User
from app.parser import ExpenseJsonOutputParser, ExpenseParser
from app.schemas import UserMessage

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
DEFAULT_API_KEY_LENGTH = 32

json_parser = ExpenseJsonOutputParser()
model = ChatAI21(model="jamba-instruct")
parser = ExpenseParser(model, json_parser)

logger = logging.getLogger("uvicorn.error")


async def create_api_key():
    session = await db.get_session()
    api_key_query = select(ApiKey)
    api_keys = await session.execute(api_key_query)
    api_keys = api_keys.scalars().first()
    if not api_keys:
        key = secrets.token_urlsafe(DEFAULT_API_KEY_LENGTH)
        api_key = ApiKey(key=key, description="Default API key")
        session.add(api_key)
        await session.commit()
        logger.info(f'Default API key created: "{key}"')
    await session.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.initialize(POSTGRES_URL)
    await create_api_key()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.post("/parse", dependencies=[Depends(validate_api_key)])
async def parse_expense(
    message: UserMessage,
    session: SessionDep,
):
    telegram_id = message.telegram_id
    user_query = select(User).where(User.telegram_id == telegram_id)
    user = await session.execute(user_query)
    user = user.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not in whitelist")

    res = await parser.parse(message.text)
    expense = Expense(
        user_id=1,
        description=res["description"],
        amount=res["price"],
        category=res["category"],
    )
    session.add(expense)
    await session.commit()
    return {"message": f"{res['category']} expense added ✅"}
