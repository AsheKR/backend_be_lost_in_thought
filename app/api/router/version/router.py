from api.depdendency import get_config
from api.router.version.string import VersionEndPoint
from api.util.header import get_app_version, get_os_name
from core.config import Config
from core.support_os import SupportOS
from fastapi import APIRouter, Depends

version_router = APIRouter()


@version_router.get(path=VersionEndPoint.can_update)
async def can_update(
    config: Config = Depends(get_config),
    app_version: str = Depends(get_app_version),
    os_name: SupportOS = Depends(get_os_name),
) -> bool:
    if os_name == SupportOS.ANDROID:
        if config.ANDROID_LATEST_VERSION > app_version:
            return True

    if os_name == SupportOS.IOS:
        if config.IOS_LATEST_VERSION > app_version:
            return True

    return False
