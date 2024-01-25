from typing import Annotated

from core.support_os import SupportOS
from fastapi import Header


async def get_os_name(
    x_os_name: Annotated[str | None, Header()] = None
) -> SupportOS | None:
    try:
        return SupportOS[x_os_name.upper()]
    except KeyError:
        pass

    return None


async def get_device_model(x_device_model: Annotated[str | None, Header()] = None) -> str | None:
    return x_device_model


async def get_app_version(x_app_version: Annotated[str | None, Header()] = None) -> str | None:
    return x_app_version
