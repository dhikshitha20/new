from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    secret_key: str = "changeme-use-a-long-random-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./taskmanager.db"

    model_config = {"env_file": ".env"}


settings = Settings()