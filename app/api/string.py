from enum import StrEnum


class RootEndPoint(StrEnum):
    docs = "/docs"
    redoc = "/redoc"
    auth = "/auth"
    question = "/question"


class APIDocString(StrEnum):
    label = "backend"
    description = "backend API"
    version = "0.0.1"
