from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ContractGuard AI"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()