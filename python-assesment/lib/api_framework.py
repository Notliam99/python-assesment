"""
Custom API Router Decorators
"""

from starlette.routing import Route, Mount  # NOTE: Important Routing CLasses


def route_fn(
    path: str,
    methods: list[str],
    context: dict,
    include_in_schema=True
):
    """Apply To functions to be turned into routes"""
    def decorator(f):
        # NOTE: Save Route Function Data To [`context`]
        context[f.__name__] = {
            "path": path,
            "methods": methods,
            "include_in_schema": include_in_schema
        }
        return f
    return decorator


def route_init(path="/"):
    """
    Apply to class initalise function to add decorated routes to self.routes
    very fancy.
    """
    def decorator(f):
        def wraper(self, *args, **kwargs):
            # NOTE: Wraper is called instead of [`f`]
            result = f(self, *args, **kwargs)  # NOTE:Run [`f`] and Save Result
            list_routes = list[Route]()  # NOTE:Save A List Of Decorated Routes
            for func_name, route_config in self.context.items():
                list_routes.append(Route(
                    path=route_config["path"],
                    endpoint=getattr(self, func_name),
                    methods=route_config["methods"],
                    include_in_schema=route_config["include_in_schema"]
                ))
            self.mount = Mount(path=path, routes=list_routes)  # NOTE:API Mount
            return result
        return wraper
    return decorator
