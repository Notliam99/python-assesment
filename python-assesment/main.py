from starlette.applications import Starlette # NOTE: ASGI Server
from starlette.routing import Route, Mount # NOTE: Routing Classes
from starlette.routing import RedirectResponse # NOTE: Redirect for `/docs`
from starlette.staticfiles import StaticFiles # NOTE: StaticFiles Serve Class
from starlette.schemas import SchemaGenerator # NOTE: OpenApi Spec Schema Gen
from hypercorn import Config # NOTE: Async WebServer Config
from hypercorn.asyncio import serve # NOTE: Compatible Server For [`asyncio`]
from lib.api import API # NOTE: Core API Class
import asyncio # NOTE: Async Runtime

# NOTE: API class
api = API()

# NOTE: base schema e.g. version title ect...
schema = SchemaGenerator({
    "openapi": "3.0.0",
    "info": {
        "title": "Python Assesment",
        "version": "0.1"
    }
})

# NOTE: api.routes list of Routes Defined by decorated functions
app = Starlette(
    routes=[
        # NOTE: Mount is the combonation of routes under one namespace
        api.mount,
        # NOTE: Bellow Routes/Mounts are related to API docs only.
        # NOTE: Swagger StaticFiles
        Mount(
            path="/docs",
            app=StaticFiles(directory="../swagger_ui"),
            name="swagger",
        ),
        # NOTE: Redirect from /docs to /docs/index.html
        Route(
            path="/docs",
            endpoint=lambda request: RedirectResponse("/docs/index.html"),
            include_in_schema=False
        ),
        # NOTE: Schema File
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
