from starlette.routing import Route, Mount

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
            self.mount = None
            for func_name, route_config in self.context.items():
                self.list_routes.append(Route(path=route_config["path"], endpoint=getattr(self, func_name), methods=route_config["methods"], include_in_schema=True))
            self.mount = Mount(path=path, routes=self.list_routes)
            return result
        return wraper
    return decorator
