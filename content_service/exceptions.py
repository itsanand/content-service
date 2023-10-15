"""Handles content service related exception"""
from typing import Union


class ContentDoesNotExistError:  # pylint: disable=too-few-public-methods
    """class for content does not exist error"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """content does not exist payload"""

        return {"code": 404, "error": "Content not Found"}


class MissingContentFile:  # pylint: disable=too-few-public-methods
    """class for content file not in body"""

    @staticmethod
    def error() -> dict[str, Union[str, int]]:
        """content file not in body"""

        return {"code": 400, "error": "Csv file is not present in the body"}


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
