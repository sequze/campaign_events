import logging
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
if not ENV_PATH.exists():
    ENV_PATH = BASE_DIR / ".env.example"


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "debug"
    log_format: str = LOG_DEFAULT_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RunConfig(BaseModel):
    reload: bool = True
    host: str = "0.0.0.0"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    campaigns: str = "/campaigns"
    events: str = "/events"


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
    logging: LoggingConfig = LoggingConfig()
    scheduler_host: str = "localhost"


settings = Settings()
