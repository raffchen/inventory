import enum
from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UpdateType(enum.Enum):
    USED = "used"
    RESTOCK = "restock"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC))


class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity_change: Mapped[int]
    new_quantity: Mapped[int]
    update_timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(UTC))
    update_type: Mapped[UpdateType]
    update_machine: Mapped[str | None]