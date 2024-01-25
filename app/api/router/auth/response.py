from pydantic import BaseModel, UUID4


class RegisterResponse(BaseModel):
    id: UUID4


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
