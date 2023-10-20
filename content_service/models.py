"""Handles database connection and tables"""
from sqlalchemy.engine.base import Engine
from sqlalchemy import (
    Column,
    String,
    create_engine,
    DateTime,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
import content_service.settings as Config

# Database Configuration
DB_ENGINE: Engine = create_engine(Config.DATABASE_URL)
BASE = declarative_base()
ASYNC_DB_ENGINE = create_async_engine(Config.ASYNC_DATABASE_URL)


# Define SQLAlchemy Models
class Content(BASE):  # type: ignore # pylint: disable=too-few-public-methods
    """Content model"""

    __tablename__ = "Content"
    title: Column = Column(String, primary_key=True)
    story: Column = Column(String)
    publishedDate: Column = Column(DateTime)
    userID: Column = Column(String)


if __name__ == "__main__":
    BASE.metadata.drop_all(DB_ENGINE)
    BASE.metadata.create_all(DB_ENGINE)
