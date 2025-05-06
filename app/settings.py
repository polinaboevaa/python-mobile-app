from pydantic import BaseSettings
from datetime import timedelta, time
from functools import lru_cache

class AppSettings(BaseSettings):
    PERIOD: timedelta = timedelta(hours=6)
    INTERVAL_HOURS: int = 14
    START_TIME: time = time(8, 0)
    TIMEZONE: str = "Europe/Kaliningrad"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
