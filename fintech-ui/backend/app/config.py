from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/fintech"
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

settings = Settings()