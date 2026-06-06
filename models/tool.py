"""
Created by shqtes on 03.06.2026.
"""
from sqlalchemy import String, Integer, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base
from decimal import Decimal


class Tool(Base):
    __tablename__ = "tools"
    __table_args__ = (
        CheckConstraint("price >= 0", name="price_greater_or_equal_zero"),
        CheckConstraint("quantity >= 0", name="quantity_greater_or_equal_zero")
    )

    tool_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(25), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(7, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
