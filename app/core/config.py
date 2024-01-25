from typing import Type

import os
from datetime import timedelta
from enum import StrEnum
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class EnvironmentKey(StrEnum):
    env = "ENV"
    debug = "DEBUG"


class Env(StrEnum):
    local = "local"
    test = "test"
    development = "development"
    production = "production"


class Config(BaseSettings):
    ENV: str
    DEBUG: bool
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    SQLALCHEMY_DATABASE_URI: PostgresDsn
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_DELTA: timedelta
    JWT_REFRESH_TOKEN_EXPIRE_DELTA: timedelta


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
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_DELTA: timedelta = timedelta(hours=7)
    JWT_REFRESH_TOKEN_EXPIRE_DELTA: timedelta = timedelta(days=7)


class TestConfig(LocalConfig):
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username="backend",
        password="backend",
        host="localhost",
        path="backend_test",
        port=5678,
    )


class DevelopmentConfig(Config):
    ENV: str = Env.development
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username="backend",
        password="backend",
        host="localhost",
        path="backend",
        port=5678,
    )
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_DELTA: timedelta = timedelta(hours=7)
    JWT_REFRESH_TOKEN_EXPIRE_DELTA: timedelta = timedelta(days=7)


class ProductionConfig(Config):
    ENV: str = Env.production
    DEBUG: bool = False
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        username="backend",
        password="backend",
        host="localhost",
        path="backend",
        port=5678,
    )
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_DELTA: timedelta = timedelta(hours=7)
    JWT_REFRESH_TOKEN_EXPIRE_DELTA: timedelta = timedelta(days=7)


@lru_cache
def get_config() -> Config:
    config = {
        Env.local: LocalConfig,
        Env.test: TestConfig,
        Env.development: DevelopmentConfig,
        Env.production: ProductionConfig,
    }[Env[os.getenv(EnvironmentKey.env, default=Env.local)]]()
    if config.ENV == Env.local:
        print(f"config : {config}")

    return config
