from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str = 'localhost'
    DATABASE_URL: str = 'postgresql:'
    DATABASE_PORT: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()