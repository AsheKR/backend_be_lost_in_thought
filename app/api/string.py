from enum import StrEnum


class EndPoint(StrEnum):
    docs = "/docs"
    redoc = "/redoc"
    user = "/users"


class APIDocString(StrEnum):
    title = "backend"
    description = "backend API"
    version = "0.0.1"
