from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_TOKEN:  str
    SECRET_KEY:   str
    ENVIRONMENT:  str = "production"

    class Config:
        env_file = ".env"   # only used in local dev

settings = Settings()
