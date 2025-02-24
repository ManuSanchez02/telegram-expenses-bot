from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User


class Expense(BaseModel):
    __tablename__ = "expenses"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    added_at: Mapped[datetime] = mapped_column(default=datetime.now)

    user: Mapped["User"] = relationship(back_populates="expenses")

    def __init__(self, user_id: int, description: str, amount: float, category: str):
        self.user_id = user_id
        self.description = description
        self.amount = amount
        self.category = category
