from starlette.applications import Starlette
from starlette.routing import Route
from starlette.schemas import SchemaGenerator
from hypercorn import Config
from hypercorn.asyncio import serve
from lib.api import API
import asyncio

# NOTE: API class
api = API()

schema = SchemaGenerator({"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}})

def openapi_schema(request):
    return schema.OpenAPIResponse(request=request)

# NOTE: api.routes list of Routes Defined by decorated functions
app = Starlette(routes=[api.mount, Route(path="/v0.1/schema.json", endpoint=openapi_schema)])

print(schema.get_schema(api.list_routes))

if __name__ == "__main__":
    config = Config()
    # NOTE: (0.0.0.0) declears any connection from any ip is ok and (:8000) defines the server port
    config.bind = ["0.0.0.0:8000"]

    # NOTE: async runtime excutes the async server
    asyncio.run(serve(app, config))
