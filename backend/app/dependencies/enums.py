import enum


class UpdateField(enum.Enum):
    NAME = "name"
    DESCRIPTION = "description"
    QUANTITY = "quantity"


class UpdateType(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
