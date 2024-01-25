from fastapi import Security
from fastapi.security import APIKeyHeader

AuthorizationHeader = Security(APIKeyHeader(name="Authorization", scheme_name="JWT"))
