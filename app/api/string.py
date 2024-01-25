from enum import StrEnum


class RootEndPoint(StrEnum):
    docs = "/docs"
    redoc = "/redoc"
    auth = "/auth"
    question = "/question"
    answer = "/answer"


class APIDocString(StrEnum):
    label = "backend"
    description = "backend API"
    version = "0.0.1"
