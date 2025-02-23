from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import Expense


class User(BaseModel):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(unique=True)

    expenses: Mapped["Expense"] = relationship(back_populates="user")

    def __init__(self, telegram_id: str):
        self.telegram_id = telegram_id
