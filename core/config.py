import os
from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings


class EnvironmentKey(StrEnum):
    env = "ENV"
    debug = "DEBUG"


class Env(StrEnum):
    local = "local"
    development = "development"
    production = "production"


class Config(BaseSettings):
    ENV: str
    DEBUG: bool
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000


class LocalConfig(Config):
    ENV: str = Env.local
    DEBUG: bool = True


class DevelopmentConfig(Config):
    ENV: str = Env.development
    DEBUG: bool = True


class ProductionConfig(Config):
    ENV: str = Env.production
    DEBUG: bool = False


@lru_cache
def get_config() -> Config:
    return {
        Env.local: LocalConfig(),
        Env.development: DevelopmentConfig(),
        Env.production: ProductionConfig(),
    }[Env[os.getenv(EnvironmentKey.env)]]
