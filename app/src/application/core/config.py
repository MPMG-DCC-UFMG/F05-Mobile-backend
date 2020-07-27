from pydantic import BaseSettings


class Settings(BaseSettings):
    sentry_key: str
    environment: str
    image_folder: str
    database_url: str
    api_prefix: str
    token_cep_aberto: str
    secret_key: str

    class Config:
        env_file = "../f05_backend.env"


settings = Settings()
