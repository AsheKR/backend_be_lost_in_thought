from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
from starlette.status import HTTP_403_FORBIDDEN

AuthorizationHeader = APIKeyHeader(name="Authorization", scheme_name="JWT")


async def get_authorization_credential(auto_error: bool = False, authorization = Security(AuthorizationHeader)) -> HTTPAuthorizationCredentials:
    scheme, credentials = get_authorization_scheme_param(authorization)
    if not (authorization and scheme and credentials):
        if auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        else:
            return None
    if scheme.lower() != "jwt":
        if auto_error:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )
        else:
            return None
    return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)
