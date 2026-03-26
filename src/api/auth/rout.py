from fastapi import (
    APIRouter, Depends, Form, HTTPException, status, Form
)
from fastapi.security import (
    HTTPAuthorizationCredentials, HTTPBearer
)
from typing import Annotated
from jwt.exceptions import InvalidKeyError, InvalidSignatureError
from shemas.shemas import UserInfo, TokenInfo, UserIn
from certs import JwtWorking, PwdWorking
from core import create_access_token, create_refresh_token
from core.helpers import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from db.crud import fake_db


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])

class TypeTokenException(Exception):
    pass

def validate_token(
    cred: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserInfo:
    try:
        data = JwtWorking.decode(cred.credentials)
        if data["type"] == REFRESH_TOKEN_TYPE: raise TypeTokenException
        if (user := fake_db.get(data["sub"])):
            return user
    except TypeTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный тип токена"
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Неправильный токен"
        )

def validate_user(
    username: str =  Form(),
    password: str = Form()
):
    if (user := fake_db.get(username)) and PwdWorking.validate_pwd(password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь не авторизован"
    )

def get_current_user_for_refresh(
    cred: HTTPAuthorizationCredentials = Depends(http_bearer)
):
    try:
        token = JwtWorking.decode(cred.credentials)
        if token["type"] == ACCESS_TOKEN_TYPE: raise TypeTokenException
        if (user := fake_db.get(token["sub"])):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован"
        )
    except TypeTokenException:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неправильный тип токена"
        )

@router.post("/login/", response_model=TokenInfo)
async def login_user(data: Annotated[UserInfo, Depends(validate_user)]):
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return TokenInfo(
        access_token=access_token, refresh_token=refresh_token
    )


@router.get("/check/", response_model=UserInfo)
async def check_token(data: Annotated[UserInfo, Depends(validate_token)]):
    return data

@router.post("/refresh/jwt", response_model=TokenInfo, response_model_exclude_none=True)
async def auth_refresh_jwt(data: Annotated[UserInfo, Depends(get_current_user_for_refresh)],):
    access_token = create_access_token(data)
    return TokenInfo(
        access_token=access_token
    )