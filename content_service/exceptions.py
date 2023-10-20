"""Handles content service related exception"""
from typing import Union


class ContentDoesNotExistError:  # pylint: disable=too-few-public-methods
    """class for content does not exist error"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """content does not exist payload"""

        return {"code": 404, "error": "Content not Found"}


class MissingFileOrUserId:  # pylint: disable=too-few-public-methods
    """class for content file not in body"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """content file or used id is required"""

        return {
            "code": 400,
            "error": "Csv file is not present in the \
            body or user id is not in query params",
        }


class InvalidPageValue:  # pylint: disable=too-few-public-methods
    """class for invalid page limit"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """invalid page limit"""

        return {"code": 400, "error": "Page value is invalid"}


class InternalCommunication:  # pylint: disable=too-few-public-methods
    """class for internal communication failure"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """internal communication failure"""

        return {"code": 500, "error": "Failed to connect with user interaction server"}


class UserDoesNotExistError:  # pylint: disable=too-few-public-methods
    """class for user does not exist error"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """user does not exist payload"""

        return {"code": 404, "error": "User not Found"}
