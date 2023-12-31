"""Handles configuration of environment variables"""
from pathlib import Path
from starlette.config import Config

CONFIG = Config(".env")
BASE_DIR = Path(__file__).parent


USER_INTERACTION_HOST = CONFIG(
    "USER_INTERACTION_HOST", cast=str, default="localhost:7000"
)
USER_SERVICE_HOST = CONFIG("USER_SERVICE_HOST", cast=str, default="localhost:8000")

DB_HOST = CONFIG("DB_HOST", cast=str, default="localhost:5432")
DB_NAME = CONFIG("DB_NAME", cast=str, default="db_content")
DB_USER = CONFIG("DB_USER", cast=str, default="postgres")
DB_PASSWORD = CONFIG("DB_PASSWORD", cast=str, default="8045")

DATABASE_URL = CONFIG(
    "DATABASE_URL",
    cast=str,
    default=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)
ASYNC_DATABASE_URL = CONFIG(
    "ASYNC_DATABASE_URL",
    cast=str,
    default=f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)
