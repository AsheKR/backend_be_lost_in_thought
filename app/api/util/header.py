from typing import Annotated

from core.maufacturer import SupportManufacturer
from fastapi import Header


async def get_device_manufacturer(
    x_device_manufacturer: Annotated[str | None, Header()] = None
) -> SupportManufacturer | None:
    try:
        return SupportManufacturer[x_device_manufacturer.upper()]
    except KeyError:
        pass

    return None


async def get_device_model(x_device_model: Annotated[str | None, Header()] = None) -> str | None:
    return x_device_model


async def get_app_version(x_app_version: Annotated[str | None, Header()] = None) -> str | None:
    return x_app_version
