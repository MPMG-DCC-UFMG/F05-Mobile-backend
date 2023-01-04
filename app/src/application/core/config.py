from pydantic import BaseSettings


class Settings(BaseSettings):
    sentry_key: str
    environment: str
    image_folder: str
    report_folder: str
    database_url: str
    api_prefix: str
    token_cep_aberto: str
    secret_key: str
    api_key: str
    system_name: str
    system_version: str
    report_institution: str
    report_department: str
    report_section: str
    report_address: str
    report_contact: str
    report_website: str

    class Config:
        env_file = "../f05_backend.env"


settings = Settings()
