from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "password123"
    DB_NAME: str = "linkedindb"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DATABASE_URL: str = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    
    SECRET_KEY: str = "this_is_a_secret"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRATION_MINUTES: int = 60


settings = Settings()