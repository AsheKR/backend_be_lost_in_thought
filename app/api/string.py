from enum import StrEnum


class EndPoint(StrEnum):
    docs = "/docs"
    redoc = "/redoc"
    auth = "/auth"
    login = "/login"
    refresh = "/refresh"


class APIDocString(StrEnum):
    label = "backend"
    description = "backend API"
    version = "0.0.1"
