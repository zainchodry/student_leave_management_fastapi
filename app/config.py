from pydantic_settings import BaseSettings
import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

class Settings(BaseSettings):

    PROJECT_NAME: str = "Student Leave Management"

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    SQLALCHEMY_DATABASE_URL: str

    MAIL_USERNAME: str

    MAIL_PASSWORD: str

    MAIL_FROM: str

    MAIL_SERVER: str

    MAIL_PORT: int

    MAIL_STARTTLS: bool = True

    MAIL_SSL_TLS: bool = False

    class Config:

        env_file = ".env"


settings = Settings()
