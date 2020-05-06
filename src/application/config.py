from pydantic import BaseSettings


class Settings(BaseSettings):
    sentry_key: str

    class Config:
        env_file = "f05_backend_dev.env"


settings = Settings()
