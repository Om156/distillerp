from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    DATABASE_PRIVATE_URL: str | None = None
    POSTGRES_URL: str | None = None
    POSTGRES_PRIVATE_URL: str | None = None
    SECRET_KEY: str | None = None
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: str = "http://localhost:5173"
    ENVIRONMENT: str = "development"
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_MINUTES: int = 15
    BACKUP_PATH: str = "./backups"

    @property
    def origins_list(self):
        origins = [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]
        return origins or ["http://localhost:5173"]

    @property
    def database_url(self) -> str:
        url = (
            self.DATABASE_URL
            or self.DATABASE_PRIVATE_URL
            or self.POSTGRES_URL
            or self.POSTGRES_PRIVATE_URL
        )
        if not url:
            raise RuntimeError(
                "Missing database URL. Set DATABASE_URL on Railway, or reference "
                "your PostgreSQL service's DATABASE_URL variable."
            )
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql://", 1)
        return url

    def validate_for_startup(self):
        missing = []
        if not (
            self.DATABASE_URL
            or self.DATABASE_PRIVATE_URL
            or self.POSTGRES_URL
            or self.POSTGRES_PRIVATE_URL
        ):
            missing.append("DATABASE_URL")
        if not self.SECRET_KEY:
            missing.append("SECRET_KEY")

        if missing:
            raise RuntimeError(
                "Missing required Railway variable(s): "
                + ", ".join(missing)
                + ". Add them in the service Variables tab, then redeploy."
            )

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
