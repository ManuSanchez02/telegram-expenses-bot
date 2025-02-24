from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.models import BaseModel


class ApiKey(BaseModel):
    __tablename__ = "api_keys"

    key: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    added_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    last_used_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

    def __init__(self, key: str, description: str):
        self.key = key
        self.description = description

    def touch(self):
        self.last_used_at = datetime.now()
