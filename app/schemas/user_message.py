from pydantic import BaseModel


class UserMessage(BaseModel):
    text: str
