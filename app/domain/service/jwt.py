from enum import StrEnum

from core.config import get_config
from core.util.jwt import JWTDecodeException, JWTExpiredException, JWTUtil
from domain.service.base import BaseService
from pydantic import BaseModel
from result import Err, Ok, Result


class JWTSubjectKey(StrEnum):
    access = "access"
    refresh = "refresh"


class JWTSchema(BaseModel):
    access_token: str
    refresh_token: str


class JWTService(BaseService):
    def __init__(self, jwt_util: JWTUtil):
        self._jwt_util = jwt_util

    def create(self, external_id: str) -> JWTSchema:
        return JWTSchema(
            access_token=self._create_access_token(external_id=external_id),
            refresh_token=self._create_refresh_token(),
        )

    def refresh(
        self, access_token: str, refresh_token: str
    ) -> Result[JWTSchema, JWTDecodeException | JWTExpiredException]:
        try:
            self._jwt_util.decode(token=access_token)
        except JWTDecodeException as e:
            return Err(e)
        except JWTExpiredException:
            pass
        else:
            return Err(JWTDecodeException())

        try:
            self._jwt_util.decode(token=refresh_token)
        except (JWTDecodeException, JWTExpiredException) as e:
            return Err(e)

        raw_access_token = self._jwt_util.decode(token=access_token, verify_exp=False)
        external_id: str | None = raw_access_token.get("id")
        if not external_id:
            return Err(JWTDecodeException())

        return Ok(
            self.create(
                external_id=external_id,
            )
        )

    def _create_access_token(self, external_id: str) -> str:
        config = get_config()
        return self._jwt_util.encode(
            subject=JWTSubjectKey.access,
            expire_delta=config.JWT_ACCESS_TOKEN_EXPIRE_DELTA,
            id=external_id,
        )

    def _create_refresh_token(self) -> str:
        config = get_config()
        return self._jwt_util.encode(
            subject=JWTSubjectKey.refresh,
            expire_delta=config.JWT_REFRESH_TOKEN_EXPIRE_DELTA,
        )
