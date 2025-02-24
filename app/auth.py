from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import select

from app.models import ApiKey

from .db import SessionDep

api_key_header = APIKeyHeader(name="X-API-Key")


async def validate_api_key(session: SessionDep, api_key_header: str = Security(api_key_header)):
    api_key = await get_api_key(session, api_key_header)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key")


async def get_api_key(session: SessionDep, api_key_header: str) -> ApiKey:
    query = select(ApiKey).where(ApiKey.key == api_key_header)
    api_key = await session.execute(query)
    api_key = api_key.scalars().first()
    if api_key is None:
        return None
    api_key.touch()
    session.add(api_key)
    await session.commit()
    return api_key
