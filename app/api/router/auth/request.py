from pydantic import UUID4, BaseModel


class LoginRequest(BaseModel):
    external_id: UUID4


class RefreshRequest(BaseModel):
    refresh_token: str
