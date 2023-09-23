from pydantic import Field
import aiosqlite

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    API_KEY: str = ""
    API_V1_STR: str = ""
    SQLALCHEMY_DATABASE_URI: str = Field(..., validation_alias='DATABASE_URL')
    SQLALCHEMY_TEST_DATABASE_URI: str = ""
    DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f"
    APP_NAME: str = ""


settings = Settings(
    # SQLALCHEMY_DATABASE_URI="postgresql+asyncpg://user:password@localhost:5432/trackfood"
    SQLALCHEMY_TEST_DATABASE_URI="sqlite+aiosqlite:///./app/tests/test.db",
    APP_NAME="Caloria"
)
