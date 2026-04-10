from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings class for validating types of env variables
class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str

    # Default settings source for local development.
    # Values passed directly to `Settings(...)` override these defaults.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    def get_db_url(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
