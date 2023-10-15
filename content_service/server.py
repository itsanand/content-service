"""Handles Content App Server"""
from starlette.applications import Starlette
from starlette.routing import Route
from content_service.endpoints.content_endpoint import ContentEndpoint
from content_service.endpoints.swagger_doc import SwaggerDoc

content_endpoint: ContentEndpoint = ContentEndpoint()
swagger_doc: SwaggerDoc = SwaggerDoc()

routes: list[Route] = [
    Route("/content", content_endpoint.create_content, methods=["POST"]),
    Route("/content/new", content_endpoint.fetch_latest_content, methods=["GET"]),
    Route("/content/top", content_endpoint.fetch_top_content, methods=["GET"]),
    Route("/content/{title}", content_endpoint.update_content, methods=["PATCH"]),
    Route("/content/{title}", content_endpoint.delete_content, methods=["DELETE"]),
    Route("/content/{title}", content_endpoint.fetch_content, methods=["GET"]),
    Route("/docs", swagger_doc.swagger_ui, methods=["GET"]),
    Route("/spec", swagger_doc.get_spec, methods=["GET"]),
]

app: Starlette = Starlette(routes=routes)
