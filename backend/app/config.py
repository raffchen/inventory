from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    log_level: str = "DEBUG"


settings = Settings()  # type: ignore
