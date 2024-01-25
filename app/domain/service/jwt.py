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
    def create(self, external_id: str) -> JWTSchema:
        return JWTSchema(
            access_token=self._create_access_token(external_id=external_id),
            refresh_token=self._create_refresh_token(),
        )

    def refresh(
        self, access_token: str, refresh_token: str
    ) -> Result[JWTSchema, JWTDecodeException | JWTExpiredException]:
        try:
            JWTUtil.decode(token=access_token)
        except JWTDecodeException as e:
            return Err(e)
        except JWTExpiredException:
            pass
        else:
            return Err(JWTDecodeException())

        try:
            JWTUtil.decode(token=refresh_token)
        except (JWTDecodeException, JWTExpiredException) as e:
            return Err(e)

        raw_access_token = JWTUtil.decode(token=access_token, verify_exp=False)
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
        return JWTUtil.encode(
            subject=JWTSubjectKey.access,
            expire_delta=config.JWT_ACCESS_TOKEN_EXPIRE_DELTA,
            id=external_id,
        )

    def _create_refresh_token(self) -> str:
        config = get_config()
        return JWTUtil.encode(
            subject=JWTSubjectKey.refresh,
            expire_delta=config.JWT_REFRESH_TOKEN_EXPIRE_DELTA,
        )

    def verify(self, token: str) -> Result[None, JWTExpiredException | JWTDecodeException]:
        try:
            JWTUtil.decode(token=token)
            return Ok(None)
        except (JWTDecodeException, JWTExpiredException) as e:
            return Err(e)
