"""Handles Content App Server"""
from starlette.applications import Starlette
from starlette.routing import Route
from content_service.endpoints.content_endpoint import ContentEndpoint

content_endpoint: ContentEndpoint = ContentEndpoint()

routes: list[Route] = [
    Route("/content", content_endpoint.create_content, methods=["POST"]),
    Route("/content/new", content_endpoint.fetch_latest_content, methods=["GET"]),
    Route("/content/{title}", content_endpoint.update_content, methods=["PATCH"]),
    Route("/content/{title}", content_endpoint.delete_content, methods=["DELETE"]),
    Route("/content/{title}", content_endpoint.fetch_content, methods=["GET"]),
]

app: Starlette = Starlette(routes=routes)
