from certs import (
    JwtWorking, PwdWorking
)
from shemas.shemas import UserInfo, UserIn, TokenInfo

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(
    token_type: str, token_data: dict,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return JwtWorking.encode(
        jwt_payload,
    )

def create_access_token(data: UserInfo) -> str:
    jwt_payload = {
        "sub": data.name,
        "username": data.name,
        "email": data.email,
        "age": data.age
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=jwt_payload)

def create_refresh_token(data: UserInfo) -> str:
    jwt_payload = {
        "sub": data.name,
    }
    return create_jwt(token_type=REFRESH_TOKEN_TYPE, token_data=jwt_payload)