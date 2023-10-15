"""Handles content services"""
import csv
from typing import Final
from io import StringIO
from dateutil import parser  # type: ignore
from sqlalchemy import update, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from content_service.models import Content


class ContentService:
    """content service class"""

    _DATA_PER_PAGE: Final[int] = 100

    def __init__(self, db_engine: AsyncEngine) -> None:
        self.async_session = sessionmaker(
            db_engine, class_=AsyncSession
        )  # type: ignore

    async def create_content_service(self, csv_obj: StringIO) -> int:
        """Create content entity and a unique id for current content
        and create a record in Content table.
        title -> replace space to underscore and all letters to lower
        """

        async with self.async_session() as db_session:  # type: ignore
            try:
                csv_datas: list = [
                    {
                        "title": row["title"].lower().replace(" ", "_"),
                        "story": row["story"],
                        "publishedDate": parser.parse(row["publishedDate"]),
                    }
                    for row in csv.DictReader(csv_obj)
                ]
                query = insert(Content).values(csv_datas)
                query = query.on_conflict_do_update(
                    index_elements=["title"],
                    set_={"story": query.excluded.story},
                )
                await db_session.execute(query)
                await db_session.commit()
                return len(csv_datas)
            except Exception as error:
                db_session.rollback()
                raise error

    async def update_content_service(self, title: str, story: str) -> dict[str, str]:
        """content service to update content details"""

        async with self.async_session() as db_session:  # type: ignore
            try:
                query = (
                    update(Content).where(Content.title == title).values(story=story)
                )
                await db_session.execute(query)
                await db_session.commit()
                return await self.read_content_service(title)
            except Exception as error:
                await db_session.rollback()
                raise error

    async def read_content_service(self, title: str) -> dict[str, str]:
        """Read content based on the content title"""

        async with self.async_session() as db_session:  # type: ignore
            content: Content = await db_session.get(Content, title)
            return {
                "title": content.title,  # type: ignore
                "story": content.story,  # type: ignore
            }

    async def delete_content_service(self, title: str) -> None:
        """Delete content record based on content title"""

        try:
            async with self.async_session() as db_session:  # type: ignore
                _: dict[str, str] = await self.read_content_service(title)
                query = delete(Content).where(Content.title == title)
                await db_session.execute(query)
                await db_session.commit()
        except Exception as error:
            await db_session.rollback()
            raise error

    async def read_latest_content(self, page: int) -> list[dict[str, str]]:
        """Fetch the latest content record sorted by date
        NOTE: 1 page contains 100 content data.
        """

        async with self.async_session() as db_session:  # type: ignore
            query = (
                select(Content)
                .order_by(Content.publishedDate.desc())
                .offset((page - 1) * self._DATA_PER_PAGE)
                .limit(page * self._DATA_PER_PAGE)
            )
            result = await db_session.execute(query)
            latest_content: list[Content] = result.scalars().all()
            return [
                {
                    "title": content.title,  # type: ignore
                    "story": content.story,  # type: ignore
                    "publishedDate": str(content.publishedDate),
                }
                for content in latest_content
            ]
