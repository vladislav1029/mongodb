from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[BASE_DIR / ".env", BASE_DIR / ".env.test"], env_file_encoding="utf-8"
    )

    DEBUG: bool = True

    MONGO_NAME: str = "notes_db"
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: Optional[str]

    MONGO_PASSWORD: Optional[str]

    @property
    def MONGO_URI(self):
        if not self.MONGO_PASSWORD or not self.MONGO_USER:
            return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"


settings = Config()
