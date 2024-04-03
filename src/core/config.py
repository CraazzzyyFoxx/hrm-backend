from pathlib import Path

from pydantic import EmailStr, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application
    project_name: str = "Dude Duck CRM"
    project_version: str = "1.0.0"
    debug: bool = False
    project_url: str = "https://crypto.asuscomm.com:8080/api/v1"
    username_regex: str = r"([a-zA-Z0-9_-]+)"

    # CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000"]'
    cors_origins: list[str] = []
    use_correlation_id: bool = False

    port: int

    # Logging
    log_level: str = "info"
    logs_root_path: str = f"{Path.cwd()}/logs"
    sentry_dsn: str | None = None

    # Postgres
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str

    # JWT
    access_token_secret: str
    refresh_token_secret: str
    reset_password_secret: str
    verify_email_secret: str
    algorithm: str = "HS256"
    expires_s: int = 3600
    access_token_audience: str = "dude_duck:access"
    verification_token_audience: str = "dude_duck:verify"
    reset_password_token_audience: str = "dude_duck:reset"
    request_verify_email_token_audience: str = "dude_duck:request_verify_email"
    discord_oauth_token_audience: str = "dude_duck:discord_oauth"

    # super user
    super_user_username: str
    super_user_email: EmailStr
    super_user_password: str

    @property
    def db_url_asyncpg(self):
        url = (
            f"{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        return f"postgresql+asyncpg://{url}"

    @property
    def db_url(self):
        url = (
            f"{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
        return f"postgresql+psycopg://{url}"


app = AppConfig(_env_file=".env", _env_file_encoding="utf-8")
