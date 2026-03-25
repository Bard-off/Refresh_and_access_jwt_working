from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict, BaseSettings
import pathlib as ptl

BASE_DIR = ptl.Path(__file__).parent.parent

class Certs(BaseModel):
    path_to_private: ptl.Path = BASE_DIR / "certs" / "private.pem"
    path_to_public: ptl.Path = BASE_DIR / "certs" / "public.pem"

class Server(BaseModel):
    allow_credentails: bool = True
    allow_origins: list = ["*"]
    allow_methods: list = ["*"]
    allow_headers: list = ["*"]
    host: str = "localhost"
    port: int = 8000
    reload: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    certs: Certs = Certs()
    server: Server = Server()



settings = Settings()