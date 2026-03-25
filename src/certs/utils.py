import jwt
import bcrypt as bc
from core import settings
from datetime import (
    datetime, timedelta
)

class JwtWorking:
    def __init__(self) -> None:
        pass
    @classmethod
    def encode(
        cls,
        payload: dict,
        private_key: str = settings.certs.path_to_private.read_text(),
        algorithm: str = "RS256",
        access_token_expire_minutes: int = 15
    ) -> str:
        now = datetime.utcnow()
        expire = now + timedelta(minutes=access_token_expire_minutes)
        payload.update(
            iat=now,
            exp=expire
        )
        encoded = jwt.encode(
            payload, private_key, algorithm=algorithm
        )
        return encoded
    @classmethod
    def decode(
        cls,
        token: str,
        public_key: str = settings.certs.path_to_public.read_text(),
        algorithm: str = "RS256",
    ) -> dict:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded


class PwdWorking:
    def __init__(self) -> None:
        pass
    @classmethod
    def hash_pdw(cls, password: str) -> bytes:
        salt = bc.gensalt()
        pwd_bytes = password.encode()
        return bc.hashpw(pwd_bytes, salt)
    @classmethod
    def validate_pwd(cls, pwd: str, pwd_hash: bytes):
        return bc.checkpw(password=pwd.encode(), hashed_password=pwd_hash)
