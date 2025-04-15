from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

from app.config import settings
from pydantic import BaseModel, ConfigDict, field_serializer


class LensRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lens_type: str
    sphere: float
    cylinder: float
    unit_price: float
    quantity: int
    storage_limit: int | None = None
    # sequence_number: int | None
    # order_sequence_number: int | None
    comment: str | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    # TODO: maybe this should be done on client side instead
    @field_serializer("created_at", "updated_at", "deleted_at")
    def convert_to_local(self, dt: datetime) -> str:
        if dt:
            local_tz = ZoneInfo(settings.local_timezone)
            return dt.astimezone(local_tz).isoformat()


class LensCreate(BaseModel):
    # TODO: allow update_source
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    lens_type: str
    sphere: Decimal
    cylinder: Decimal
    unit_price: Decimal
    quantity: int = 0
    storage_limit: int | None = None
    # sequence_number: int | None
    # order_sequence_number: int | None
    comment: str | None = None


class LensUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    unit_price: Decimal | None = None
    quantity: int | None = None
    storage_limit: int | None = None
    comment: str | None = None
    updated_at: datetime | None = None
    update_notes: str | None = None
    update_source: str | None = None
