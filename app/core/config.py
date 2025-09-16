from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "password123"
    DB_NAME: str = "linkedindb"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    SECRET_KEY: str = "this_is_a_secret"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRATION_MINUTES: int = 60

    @computed_field 
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"

settings = Settings()

print(settings.DB_USERNAME)   # -> from .env
print(settings.DATABASE_URL)  # -> built from .env values
