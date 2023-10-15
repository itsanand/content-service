"""Handles endpoints for content service"""
from typing import Final
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.datastructures import UploadFile
from io import StringIO
from content_service.exceptions import (
    MissingContentFile,
    ContentDoesNotExistError,
    InvalidPageValue,
)
from content_service.services.content_service import ContentService

from content_service.models import ASYNC_DB_ENGINE


class ContentEndpoint:
    """endpoint class to handle content services"""

    svc: ContentService = ContentService(ASYNC_DB_ENGINE)
    BAD_REQUEST: Final[int] = 400
    SUCCESS: Final[int] = 200
    CREATED: Final[int] = 201
    NOT_FOUND: Final[int] = 404

    @classmethod
    async def create_content(cls, request: Request) -> JSONResponse:
        """Handles create content service"""

        try:
            form_data = await request.form()
            assert isinstance(form_data["content"], UploadFile)
            csv_file: UploadFile = form_data["content"]
            csv_data: StringIO = StringIO((await csv_file.read()).decode("UTF-8"))
            data_count: int = await cls.svc.create_content_service(csv_data)
            return JSONResponse(
                {"msg": f"{data_count} data added"}, status_code=cls.CREATED
            )
        except KeyError:
            return JSONResponse(MissingContentFile.error(), status_code=cls.BAD_REQUEST)

    @classmethod
    async def update_content(cls, request: Request) -> JSONResponse:
        """Handles update content service"""

        try:
            title: str = request.path_params["title"].lower().replace(" ", "_")
            body: bytes = await request.body()
            content = await cls.svc.update_content_service(title, body.decode("utf-8"))
            return JSONResponse(content, status_code=cls.SUCCESS)
        except AttributeError:
            return JSONResponse(
                ContentDoesNotExistError.error(), status_code=cls.NOT_FOUND
            )

    @classmethod
    async def delete_content(cls, request: Request) -> JSONResponse:
        """Handles delete content service"""

        try:
            title: str = request.path_params["title"].lower().replace(" ", "_")
            await cls.svc.delete_content_service(title)
            return JSONResponse(None, status_code=cls.SUCCESS)
        except AttributeError:
            return JSONResponse(
                ContentDoesNotExistError.error(), status_code=cls.NOT_FOUND
            )

    @classmethod
    async def fetch_content(cls, request: Request) -> JSONResponse:
        """Handles fetch content service"""

        try:
            title: str = request.path_params["title"].lower().replace(" ", "_")
            content: dict[str, str] = await cls.svc.read_content_service(title)
            return JSONResponse(content, status_code=cls.SUCCESS)
        except AttributeError:
            return JSONResponse(
                ContentDoesNotExistError.error(), status_code=cls.NOT_FOUND
            )

    @classmethod
    async def fetch_latest_content(cls, request: Request) -> JSONResponse:
        """Handles fetch latest contents"""

        try:
            page: str = request.query_params.get("page", "1")
            content: list[dict[str, str]] = await cls.svc.read_latest_content(int(page))
            return JSONResponse(content, status_code=cls.SUCCESS)
        except TypeError:
            return JSONResponse(InvalidPageValue.error(), status_code=cls.BAD_REQUEST)

    @classmethod
    async def fetch_top_content(cls, request: Request) -> JSONResponse:
        """Handled fetch top contents"""

        try:
            page: str = request.query_params.get("page", "1")
            content: list[dict[str, str | int]] = await cls.svc.read_top_content(
                int(page)
            )
            return JSONResponse(content, status_code=cls.SUCCESS)
        except TypeError:
            return JSONResponse(InvalidPageValue.error(), status_code=cls.BAD_REQUEST)
