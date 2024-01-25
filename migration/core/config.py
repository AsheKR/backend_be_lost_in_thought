import os
from enum import StrEnum
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class EnvironmentKey(StrEnum):
    env = "ENV"


class Env(StrEnum):
    local = "local"
    test = "test"
    development = "development"
    production = "production"


class Config(BaseSettings):
    ENV: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn


class LocalConfig(Config):
    ENV: str = Env.local
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        username="backend",
        password="backend",
        host="localhost",
        path="backend",
        port=5678,
    )


class TestConfig(LocalConfig):
    SQLALCHEMY_DATABASE_URI: PostgresDsn = PostgresDsn.build(
        scheme="postgresql",
        username="backend",
        password="backend",
        host="localhost",
        path="backend_test",
        port=5678,
    )


class DevelopmentConfig(Config):
    ENV: str = Env.development


class ProductionConfig(Config):
    ENV: str = Env.production


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
