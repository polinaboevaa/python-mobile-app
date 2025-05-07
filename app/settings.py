from pydantic_settings import BaseSettings
from datetime import timedelta, time
from functools import lru_cache

class AppSettings(BaseSettings):
    PERIOD: timedelta = timedelta(hours=6)
    INTERVAL_HOURS: int = 14
    START_TIME: time = time(8, 0)
    TIMEZONE: str = "Europe/Kaliningrad"

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        env_prefix = "APP_"

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
