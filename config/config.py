from functools import lru_cache
from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Keyword Registry Service"
    mongo_url: str
    secret_key: str
    model_config = SettingsConfigDict(env_file=".env",  env_file_encoding='utf-8')

@lru_cache
def get_settings():
    return Settings()