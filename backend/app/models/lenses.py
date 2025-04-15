from enum import Enum
from datetime import datetime
from decimal import Decimal

from sqlalchemy import TIMESTAMP, ForeignKey, func, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class UpdateField(Enum):
    LENS_TYPE = "lens_type"
    SPHERE = "sphere"
    CYLINDER = "cylinder"
    UNIT_PRICE = "unit_price"
    QUANTITY = "quantity"
    STORAGE_LIMIT = "storage_limit"
    COMMENT = "comment"
    DELETED_AT = "deleted_at"


class UpdateType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Lenses(Base):
    __tablename__ = "lenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lens_type: Mapped[str]
    sphere: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    cylinder: Mapped[Decimal] = mapped_column(Numeric(4, 2))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    quantity: Mapped[int]
    storage_limit: Mapped[int | None]
    # sequence_number: Mapped[int | None]
    # order_sequence_number: Mapped[int | None]
    comment: Mapped[str | None]
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


class LensesHistory(Base):
    __tablename__ = "lenses_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    lens_id: Mapped[int] = mapped_column(ForeignKey("lenses.id"))
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
