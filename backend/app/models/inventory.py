from enum import Enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UpdateField(Enum):
    NAME = "name"
    DESCRIPTION = "description"
    QUANTITY = "quantity"
    DELETED_AT = "deleted_at"


class UpdateType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    quantity: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))


class ProductHistory(Base):
    __tablename__ = "product_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    update_field: Mapped[UpdateField]
    old_value: Mapped[str | None]
    new_value: Mapped[str | None]
    update_timestamp: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    update_type: Mapped[UpdateType]
    update_notes: Mapped[str | None]
    update_source: Mapped[str | None]
