import os
from enum import StrEnum
from functools import lru_cache

from pydantic import PostgresDsn
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
    SQLALCHEMY_DATABASE_URI: PostgresDsn


class LocalConfig(Config):
    ENV: str = Env.local
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username="backend",
        password="backend",
        host="localhost",
        path="backend",
        port=5678,
    )


class DevelopmentConfig(Config):
    ENV: str = Env.development
    DEBUG: bool = True


class ProductionConfig(Config):
    ENV: str = Env.production
    DEBUG: bool = False


@lru_cache
def get_config() -> Config:
    config = {
        Env.local: LocalConfig,
        Env.development: DevelopmentConfig,
        Env.production: ProductionConfig,
    }[Env[os.getenv(EnvironmentKey.env)]]()
    if config.ENV == Env.local:
        print(f"config : {config}")

    return config
