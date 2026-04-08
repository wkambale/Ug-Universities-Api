from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_TOKEN:  str
    SECRET_KEY:   str
    ENVIRONMENT:  str = "production"

    model_config = ConfigDict(env_file=".env")  # only used in local dev

settings = Settings()
