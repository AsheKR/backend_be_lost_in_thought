from enum import StrEnum

from fastapi import APIRouter

health_check_router = APIRouter()


class HealthCheckEndPoint(StrEnum):
    default = ''


@health_check_router.get(HealthCheckEndPoint.default)
def default() -> bool:
    return True
