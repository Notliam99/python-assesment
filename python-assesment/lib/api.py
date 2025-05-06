from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.schemas import SchemaGenerator

# NOTE: decorators Are Working
# TODO: Add nested paths to route_init

def route_fn(path: str, methods: list[str], context: dict):
    """
    Apply To functions to be turned into routes
    """
    def decorator(f):
        async def wraper(self, request):
            return await f(self, request)
        context[f.__name__] = {"path": path, "methods": methods}
        return wraper
    return decorator

def route_init(path="/"):
    """
    Apply to class initalise function to add decorated routes to self.routes
    """
    def decorator(f):
        def wraper(self, *args, **kwargs):
            result = f(self, *args, **kwargs)
            for func_name, route_config in self.context.items():
                # TODO: Nested path Routing
                self.routes.append(Route(path=route_config["path"], endpoint=getattr(self, func_name), methods=route_config["methods"]))
            return result
        return wraper
    return decorator

class API:
    """
    To Use As Super Must Create A Dictionary Called "context"
    """
    context = dict()

    @route_init(path="/")
    def __init__(self):
        """
        Initalise Class to use this class must use the example setup showen here
        """
        self.routes = list[Route]()

        self.schemas = SchemaGenerator({"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}})

    @route_fn(path="/hello", methods=["GET"], context=context)
    async def hello_world(self, request) -> dict:
        """
        responses:
            200:
                description: hello
                examples:
                    hello
        """
        return JSONResponse({"message": "hello_world"})
