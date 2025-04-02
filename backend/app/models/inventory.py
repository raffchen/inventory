from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]


class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity_change: Mapped[int]
    new_quantity: Mapped[int]
    update_timestamp: Mapped[datetime] = mapped_column(insert_default=func.now())
    update_type: Mapped[str]
    update_machine: Mapped[str | None]