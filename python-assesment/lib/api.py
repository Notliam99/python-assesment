from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.schemas import SchemaGenerator
from starlette.requests import HTTPConnection, HTTPException
import typing

# NOTE: decorators Are Working

def route_fn(path: str, methods: list[str], context: dict):
    """
    Apply To functions to be turned into routes
    """
    def decorator(f):
        context[f.__name__] = {"path": path, "methods": methods}
        return f
    return decorator

def route_init(path="/"):
    """
    Apply to class initalise function to add decorated routes to self.routes
    """
    def decorator(f):
        def wraper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            self.list_routes = list[Route]()
            for func_name, route_config in self.context.items():
                # TODO: Nested path Routing
                self.list_routes.append(Route(path=route_config["path"], endpoint=getattr(self, func_name), methods=route_config["methods"], include_in_schema=True))
            self.mount = Mount(path=path, routes=self.list_routes)
            return result
        return wraper
    return decorator

class API:
    """
    To Use As Super Must Create A Dictionary Called "context"
    """
    context = dict()

    @route_init(path="/hello")
    def __init__(self):
        """
        Initalise Class to use this class must use the example setup showen here
        """
        self.list_routes = None
        self.mount = None

    @route_fn(path="/hello", methods=["GET"], context=context)
    async def hello_world(self, request: HTTPConnection) -> JSONResponse:
        """
        responses:
            200:
                description: hello
                examples:
                    hello
        """
        return JSONResponse({"message": "hello_world"})

    @route_fn(path="/hello_name", methods=["GET"], context=context)
    async def hello_name(self, request) -> JSONResponse:
        try:
            return JSONResponse({"message": {"hello": request.query_params["name"]}})
        except KeyError:
            raise HTTPException(status_code=400, detail="Bad/Malformed Request")
