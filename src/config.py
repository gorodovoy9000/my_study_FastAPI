from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # DB
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_ECHO: bool = False

    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    # REDIS_USER: str = None
    # REDIS_PASS: str = None
    # REDIS_DB_NAME: int = 0

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # media files
    LOCAL_MEDIA_ROOT: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
