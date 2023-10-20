"""Handles Content App Server"""
from sqlalchemy import inspect
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from content_service.endpoints.content_endpoint import ContentEndpoint
from content_service.endpoints.swagger_doc import SwaggerDoc
from content_service.models import BASE, DB_ENGINE

content_endpoint: ContentEndpoint = ContentEndpoint()
swagger_doc: SwaggerDoc = SwaggerDoc()

routes: list[Route] = [
    Route("/content", content_endpoint.create_content, methods=["POST"]),
    Route("/content/new", content_endpoint.fetch_latest_content, methods=["GET"]),
    Route("/content/top", content_endpoint.fetch_top_content, methods=["GET"]),
    Route("/content/{title}", content_endpoint.update_content, methods=["PATCH"]),
    Route("/content/{title}", content_endpoint.delete_content, methods=["DELETE"]),
    Route("/content/{title}", content_endpoint.fetch_content, methods=["GET"]),
    Route("/content-service/docs", swagger_doc.swagger_ui, methods=["GET"]),
    Route("/content-service/spec", swagger_doc.get_spec, methods=["GET"]),
]


def on_startup():
    """Check if table exist or not and create table"""
    inspector = inspect(DB_ENGINE)
    if not inspector.has_table("Content"):
        BASE.metadata.create_all(DB_ENGINE)


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

app: Starlette = Starlette(routes=routes, middleware=middleware)

app.add_event_handler("startup", on_startup)
