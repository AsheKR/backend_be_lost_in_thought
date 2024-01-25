from enum import StrEnum


class RootEndPoint(StrEnum):
    docs = "/docs"
    redoc = "/redoc"
    auth = "/auth"
    question = "/question"
    answer = "/answer"
    delete_all = "/delete-all"
    version = "/can-update"
    health_check = "/health-check"


class APIDocString(StrEnum):
    label = "backend"
    description = "backend API"
    version = "0.0.1"
