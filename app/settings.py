from pydantic_settings import BaseSettings
from datetime import timedelta, time
from functools import lru_cache

class BaseAppSettings(BaseSettings):
    PERIOD: timedelta = timedelta(hours=96)
    INTERVAL_HOURS: int = 14
    START_TIME: time = time(8, 0)
    TIMEZONE: str = "Europe/Kaliningrad"

    class Config:
        env_file = ".env.core"
        env_prefix = "APP_CORE_"


class DatabaseSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str

    class Config:
        env_file = ".env"
        env_prefix = "APP_DB_"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASS}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )

@lru_cache
def get_base_settings() -> BaseAppSettings:
    return BaseAppSettings()

@lru_cache
def get_settings() -> DatabaseSettings:
    return DatabaseSettings()

