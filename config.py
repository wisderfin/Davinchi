from pydantic_settings import BaseSettings


# схема переменного окружения
class Settings(BaseSettings):
    # postgres
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str

    # telegram
    TG_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()