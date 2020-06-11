from pydantic import BaseSettings


class Settings(BaseSettings):
    sentry_key: str
    environment: str
    image_folder: str

    class Config:
        env_file = "f05_backend.env"


settings = Settings()
