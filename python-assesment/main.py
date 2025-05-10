from starlette.applications import Starlette # NOTE: ASGI Server
from starlette.routing import Route, Mount # NOTE: Routing Classes
from starlette.routing import RedirectResponse # NOTE: Redirect for `/docs`
from starlette.staticfiles import StaticFiles # NOTE: StaticFiles Serve Class
from starlette.schemas import SchemaGenerator # NOTE: OpenApi Spec Schema Gen
from hypercorn import Config # NOTE: Async WebServer Config
from hypercorn.asyncio import serve # NOTE: Compatible Server For [`asyncio`]
from lib.api import API # NOTE: Core API Class
import asyncio # NOTE: Async Runtime
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi.scalar_fastapi import Layout

# NOTE: API class
api = API()
project_description = """
# Wellcome To The API Docs
***
This API is part of a school project called
[AS91906](https://www.nzqa.govt.nz/nqfdocs/ncea-resource/achievements/2024/as91906.pdf)
if your from the future this will likely no longer exist. The rough idea is to
build a complex python application like this one.
"""

# NOTE: base schema e.g. version title ect...
schema = SchemaGenerator({
    "openapi": "3.0.0",
    "info": {
        "title": "Python Assesment",
        "version": "0.1",
        "summary": "Best API So Far Of 2025",
        "description": project_description,
        "contact": {
            "name": "Liam Tietjens",
            "email": "liam@nzdev.org"
        },
        "license": {
            "name": "GNU Affero General Public License v3.0",
            "identifier": "AGPL-3.0",
            "url": "https://opensource.org/license/agpl-v3"
        },
    },
    "servers": {
        "url": "http://localhost:8000/",
        "description": "local server url"
    },
    "externalDocs": {
        "description": "GitHub Repository",
        "url": "https://github.com/Notliam99/python-assesment.git"
    }
})

# NOTE: api.routes list of Routes Defined by decorated functions
app = Starlette(
    routes=[
        # NOTE: Mount is the combonation of routes under one namespace
        api.mount,
        # NOTE: Bellow Routes/Mounts are related to API docs only.
        # NOTE: Scalar api client
        Route(
            path="/docs",
            endpoint=lambda request: get_scalar_api_reference(
                openapi_url="/v0.1/schema.json",
                title="hello",
                layout=Layout.MODERN,
                scalar_theme=""
            )
        ),
        # NOTE: Route With OpenAPI(3.0) Schema
        Route(
            path="/v0.1/schema.json",
            endpoint=lambda request: schema.OpenAPIResponse(request=request),
            include_in_schema=False
        ),
    ]
)

if __name__ == "__main__":
    config = Config()
    # NOTE: (0.0.0.0) allows any any ip and (:8000) defines the server port
    config.bind = ["0.0.0.0:8000"]

    # NOTE: async runtime excutes the async server
    asyncio.run(serve(app, config))
