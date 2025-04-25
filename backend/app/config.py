import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = False
    log_level: int = logging.WARNING
    local_timezone: str = "America/Los_Angeles"


settings = Settings()  # type: ignore
