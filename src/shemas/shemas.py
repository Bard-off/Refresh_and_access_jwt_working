from pydantic import BaseModel

class UserIn(BaseModel):
    name: str
    password: str

class UserInfo(BaseModel):
    name: str
    password:  bytes
    email: str
    age: int

class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    type: str = "Bearer"
