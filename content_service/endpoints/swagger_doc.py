"""Handles swagger docs endpoint"""
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse


class SwaggerDoc:
    """class to handle swagger doc"""

    async def swagger_ui(self, _: Request) -> HTMLResponse:
        """Handles html snippet for swagger doc"""

        with open(
            r"..\content_service\static\swagger_ui.html", encoding="utf-8"
        ) as file:
            html_code: str = file.read()
        return HTMLResponse(html_code)

    async def get_spec(self, _: Request) -> FileResponse:
        """Handles yaml code for swagger doc"""

        return FileResponse(
            path=r"..\content_service\static\swagger.yaml", filename="openapi.yaml"
        )
