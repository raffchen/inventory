import enum


class UpdateField(enum.Enum):
    NAME = "name"
    DESCRIPTION = "description"
    QUANTITY = "quantity"
    DELETED_AT = "deleted_at"


class UpdateType(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
