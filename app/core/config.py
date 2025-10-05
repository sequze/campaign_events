from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

if not ENV_PATH.exists():
    ENV_PATH = BASE_DIR / ".env.example"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class AuthJWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "app" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    refresh_token_expire_days: int = 30
    access_token_expire_minutes: int = 15


class DatabaseConfig(BaseModel):
    user: str
    password: str
    name: str
    host: str
    port: int
    echo: bool = False
    pool_size: int = 50
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        extra="ignore",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
    )
    run: RunConfig = RunConfig()
    api_prefix: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    db: DatabaseConfig


settings = Settings()
