from enum import StrEnum


class AuthEndPoint(StrEnum):
    login = "/login"
    register = "/register"
    refresh = "/refresh"
