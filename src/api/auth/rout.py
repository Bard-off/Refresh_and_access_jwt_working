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


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(dependencies=[Depends(http_bearer)])



john = UserInfo(name="ivan", password=PwdWorking.hash_pdw("1234"), email="ivan@gmail.com", age=20)
sam = UserInfo(name="sam", password=PwdWorking.hash_pdw("qwerty"), email="sam@gmail.com", age=25)

fake_db = {
    john.name: john,
    sam.name: sam
}

def validate_token(
    cred: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserInfo:
    try:
        data = JwtWorking.decode(cred.credentials)
        if (user := fake_db.get(data["sub"])):
            return user
    except InvalidSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Неправильный токен"
        )

def validate_user(
    username: str =  Form(),
    password: str = Form()              ):
    if (user := fake_db.get(username)) and PwdWorking.validate_pwd(password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Пользователь не авторизован"
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