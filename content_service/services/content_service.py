"""Handles content services"""
import csv
from typing import Final
from httpx import AsyncClient, Response
from io import StringIO
from dateutil import parser  # type: ignore
from sqlalchemy import update, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from content_service.models import Content
import content_service.settings as Config


class ContentService:
    """content service class"""

    DATA_PER_PAGE: Final[int] = 100
    SUCCESS: Final[int] = 200
    INTERNAL_HEADERS: dict[str, str] = {
        "x-internal": "groot",
    }

    def __init__(self, db_engine: AsyncEngine) -> None:
        self.async_session = sessionmaker(
            db_engine, class_=AsyncSession
        )  # type: ignore

    @classmethod
    async def user_exists(cls, user_id: str) -> bool:
        """check if user exists in user service repo"""

        async with AsyncClient() as client:
            url: str = f"http://{Config.USER_SERVICE_HOST}/user/{user_id}"
            user: Response = await client.get(
                url, headers=cls.INTERNAL_HEADERS, timeout=10.0
            )
            return user.status_code == cls.SUCCESS

    async def create_content_service(self, csv_obj: StringIO, user_id: str) -> int:
        """Create content entity and a unique id for current content
        and create a record in Content table.
        title -> replace space to underscore and all letters to lower
        """

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            try:
                csv_datas: list = [
                    {
                        "title": row["title"].lower().replace(" ", "_"),
                        "story": row["story"],
                        "publishedDate": parser.parse(row["publishedDate"]),
                        "userID": user_id,
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

    async def update_content_service(
        self, title: str, story: str, user_id: str
    ) -> dict[str, str]:
        """content service to update content details"""

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            try:
                query = (
                    update(Content).where(Content.title == title).values(story=story)
                )
                await db_session.execute(query)
                await db_session.commit()
                return await self.read_content_service(title, user_id)
            except Exception as error:
                await db_session.rollback()
                raise error

    async def read_content_service(self, title: str, user_id: str) -> dict[str, str]:
        """Read content based on the content title"""

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            content: Content = await db_session.get(Content, title)
            return {
                "title": content.title,  # type: ignore
                "story": content.story,  # type: ignore
            }

    async def delete_content_service(self, title: str, user_id: str) -> None:
        """Delete content record based on content title"""

        if not await self.user_exists(user_id):
            raise ValueError
        try:
            async with self.async_session() as db_session:  # type: ignore
                _: dict[str, str] = await self.read_content_service(title, user_id)
                query = delete(Content).where(Content.title == title)
                await db_session.execute(query)
                await db_session.commit()
        except Exception as error:
            await db_session.rollback()
            raise error

    async def read_latest_content(
        self, page: int, user_id: str
    ) -> list[dict[str, str]]:
        """Fetch the latest content record sorted by date
        NOTE: 1 page contains 100 content data.
        """

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            query = (
                select(Content)
                .order_by(Content.publishedDate.desc())
                .offset((page - 1) * self.DATA_PER_PAGE)
                .limit(page * self.DATA_PER_PAGE)
            )
            result = await db_session.execute(query)
            latest_content: list[Content] = result.scalars().all()
            return [
                {
                    "title": content.title,  # type: ignore
                    "story": content.story,  # type: ignore
                    "publishedDate": str(content.publishedDate),
                    "userID": content.userID,  # type: ignore
                }
                for content in latest_content
            ]

    async def read_top_content(
        self, page: int, user_id: str
    ) -> list[dict[str, str | int]]:
        """Fetch the top content record sorted by read and likes
        Send an api call to user interaction server to fetch content
        read and likes for each content and then sort them and returns
        based on page number.
        NOTE: 1 page contains 100 content data.
        """

        if not await self.user_exists(user_id):
            raise ValueError
        async with self.async_session() as db_session:  # type: ignore
            async with AsyncClient() as client:
                url: str = f"http://{Config.USER_INTERACTION_HOST}/contents?page={page}"
                response: Response = await client.get(
                    url, headers=self.INTERNAL_HEADERS, timeout=10.0
                )
                if response.status_code != self.SUCCESS:
                    raise ValueError("Error while fetching read and likes")
                read_like_list: list[dict[str, str | int]] = response.json()
            titles: list[str] = [
                each_data["title"] for each_data in read_like_list  # type: ignore
            ]
            query = select(
                Content.title,
                Content.story,
                Content.publishedDate,
                Content.userID,
            ).filter(Content.title.in_(titles))
            content = await db_session.execute(query)
            db_data: list[Content] = content.all()
            curr_data_len: int = len(db_data)
            if curr_data_len < (page * self.DATA_PER_PAGE):
                query = (
                    select(
                        Content.title,
                        Content.story,
                        Content.publishedDate,
                        Content.userID,
                    )
                    .filter(Content.title.not_in(titles))
                    .offset((page - 1) * self.DATA_PER_PAGE)
                    .limit((page * self.DATA_PER_PAGE) - curr_data_len)
                )
                content = await db_session.execute(query)
                db_data += content.all()
            content_dict: dict[str, Content] = {
                data.title: data for data in db_data  # type: ignore
            }
            response_data: list[dict[str, str | int]] = [
                {
                    "title": content["title"],  # type: ignore
                    "story": content_dict[content["title"]].story,  # type: ignore
                    "publishedDate": str(content_dict[content["title"]].publishedDate),
                    "userID": content_dict[content["title"]].userID,  # type: ignore
                    "totalReads": content["totalReads"],
                    "totalLikes": content["totalLikes"],
                }
                for content in read_like_list
            ]
            response_data += [
                {
                    "title": title,  # type: ignore
                    "story": content.story,  # type: ignore
                    "publishedDate": str(content.publishedDate),
                    "userID": content.userID,  # type: ignore
                    "totalReads": 0,
                    "totalLikes": 0,
                }
                for title, content in content_dict.items()
            ]
            return response_data
