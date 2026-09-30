from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/search"
    elasticsearch_url: str = "http://localhost:9200"
    es_index: str = "documents"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()