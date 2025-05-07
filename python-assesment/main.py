from starlette.applications import Starlette
from hypercorn import Config
from hypercorn.asyncio import serve
from lib.api import API
import asyncio

# NOTE: API class
api = API()

# NOTE: api.routes list of Routes Defined by decorated functions
app = Starlette(routes=[api.mount])

if __name__ == "__main__":
    config = Config()
    # NOTE: (0.0.0.0) declears any connection from any ip is ok and (:8000) defines the server port
    config.bind = ["0.0.0.0:8000"]

    # NOTE: async runtime excutes the async server
    asyncio.run(serve(app, config))
