"""Handles endpoints for content service"""
from starlette.requests import Request


class ContentEndpoint:
    """endpoint class to handle content services"""

    @classmethod
    async def create_content(cls, _: Request) -> None:
        """Handles create content service"""

        raise NotImplementedError()

    @classmethod
    async def update_content(cls, _: Request) -> None:
        """Handles update content service"""

        raise NotImplementedError()

    @classmethod
    async def delete_content(cls, _: Request) -> None:
        """Handles delete content service"""

        raise NotImplementedError

    @classmethod
    async def fetch_content(cls, _: Request) -> None:
        """Handles fetch content service"""

        raise NotImplementedError()
