from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import settings
from pydantic import BaseModel, ConfigDict, field_serializer


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    quantity: int
    created_at: datetime
    updated_at: datetime

    # TODO: maybe this should be done on client side instead
    @field_serializer("created_at", "updated_at")
    def convert_to_local(self, dt: datetime) -> str:
        local_tz = ZoneInfo(settings.local_timezone)
        return dt.astimezone(local_tz).isoformat()


class ProductReadFull(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    quantity: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    # TODO: maybe this should be done on client side instead
    @field_serializer("created_at", "updated_at", "deleted_at")
    def convert_to_local(self, dt: datetime | None) -> str:
        if dt is None:
            return

        local_tz = ZoneInfo(settings.local_timezone)
        return dt.astimezone(local_tz).isoformat()


class ProductCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    name: str
    description: str | None = None
    quantity: int


class ProductUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    name: str | None = None
    description: str | None = None
    quantity: int | None = None
    updated_at: datetime | None = None
    update_notes: str | None = None
    update_source: str | None = None
