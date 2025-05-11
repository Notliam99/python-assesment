from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.schemas import SchemaGenerator
from starlette.requests import HTTPConnection, HTTPException
from lib.api_framework import route_init, route_fn
import typing
from typing import Annotated

class API:
    """
    To Use As Super Must Create A Dictionary Called "context"
    """
    # NOTE: Important to give [`lib.api_framework.route_init`] context of Routes
    context = dict()

    @route_init(path="/hello")
    def __init__(self):
        """
        Initalise Class to use this class must use the example setup showen here
        """
        # NOTE: varibles bellow just intialised here for clarity.
        self.list_routes = None
        self.mount = None

    @route_fn(path="/hello_name", methods=["GET"], context=context)
    async def hello_name(self, request) -> JSONResponse:
        """
        summary: say hello to person by taking their name
        description: |
            # Hello!!!

            Have you or someone you know ever wanted to say hello but cant.
            *Well this is the route for you. 👍*
        parameters:
            - name: name
              in: query
              required: true
              schema:
                type: string
              description:
                Name Of Person
        responses:
            200:
                description: saying hello
                content:
                    application/json:
                        schema:
                            type: object
                            description: Message Object
                            required:
                                - "message"
                            properties:
                                message:
                                    type: object
                                    required:
                                        - "hello"
                                    properties:
                                        hello:
                                            type: string
                                            default: "<Name>"
        """
        try:
            # NOTE: Could return a error if qurey pram not found
            return JSONResponse({
                "message": {"hello": request.query_params["name"]}
            })
        except KeyError: # NOTE: Catch possible Error
            raise HTTPException(status_code=400, detail="Bad/Malformed Request")
