from api.depdendency import get_config
from api.router.version.string import VersionEndPoint
from api.util.header import get_app_version, get_device_manufacturer
from core.config import Config
from core.maufacturer import SupportManufacturer
from fastapi import APIRouter, Depends

version_router = APIRouter()


@version_router.get(path=VersionEndPoint.can_update)
async def can_update(
    config: Config = Depends(get_config),
    app_version: str = Depends(get_app_version),
    device_manufacturer: SupportManufacturer = Depends(get_device_manufacturer),
) -> bool:
    if device_manufacturer == SupportManufacturer.ANDROID:
        if config.ANDROID_LATEST_VERSION > app_version:
            return True

    if device_manufacturer == SupportManufacturer.IOS:
        if config.IOS_LATEST_VERSION > app_version:
            return True

    return False
