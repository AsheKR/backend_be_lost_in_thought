from enum import StrEnum


class AuthEndPoint(StrEnum):
    login = "/login"
    refresh = "/refresh"
