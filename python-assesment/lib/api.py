# NOTE: Responses types
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount # NOTE: Routing types/classes
from starlette.requests import HTTPException, Request # NOTE: Request/Error Type
from json.decoder import JSONDecodeError # NOTE: Exeption Type
from lib.api_framework import route_init, route_fn # NOTE: Custom API Router
from lib.person import Person # NOTE: Custom Person Type
from typing import Annotated # NOTE: Annotate Function Parameters

class API:
    """
    API Class + Custom Router Accesable at `/api`
    """
    # NOTE: Important to give [`lib.api_framework.route_init`] context of Routes
    context = dict()

    @route_init(path="/api")
    def __init__(self, people: Annotated[list[Person], "List Of Registed People"]):
        """
        Initalise Class to use this class must use the example setup showen here
        """
        self.people = people

        # NOTE: varibles bellow just intialised here for clarity.
        self.list_routes = None
        self.mount = None

    @route_fn(path="/create", methods=["POST"], context=context)
    async def add_person(self, request: Annotated[Request, "Request Data"]):
        """
        summary: Create New Person In Memory
        description: |
            # Create Person

            This route takes their name, email and optionaly a profile image.
            With these parameters writes to a object stored in memory for later
            qureys.
        requestBody:
            description: Creation Request Body
            required: true
            content:
                application/json:
                    schema:
                        description: Person Json Object
                        type: object
                        required:
                            - "name"
                            - "email"
                        properties:
                            name:
                                type: string
                                description: |
                                    Name of the user e.g. "jeff" this is
                                    **required**
                            email:
                                type: string
                                description: |
                                    Email for contact e.g.
                                    "[example@example.com](mailto:example@example.com)"
                                    this is **Required**
                            image:
                                type: string
                                description: |
                                    Base64 encoded image e.g.
                                    "https://upload.wikimedia.org/wikipedia/commons/1/1c/A_Daisy_flower.jpg"
                                    this is **Optional**.
        responses:
            200:
                description: User Was Created
                content:
                    application/json:
                        schema:
                            type: object
                            required:
                                - "message"
                            properties:
                                message:
                                    type: string
                                    example: "User Was Created"
            400:
                description: Request Malformed
                content:
                    text/plain:
                        schema:
                            type: string
                            default: "Bad/Malformed Request"
        """
        # NOTE: Sanity Check
        try:
            body = await request.json()
        except JSONDecodeError as error:
            raise HTTPException(status_code=400, detail=f"Bad/Malformed Request Error: '{error}'")

        # NOTE: Input Validation
        try:
            if (name := body["name"]) == "":
                raise KeyError("Key: [`name`] Incorectly Set")
            if (email := body["email"]) == "":
                raise KeyError("Key: [`email`] Incorectly Set")
        except KeyError as error:
            raise HTTPException(status_code=400, detail=f"Bad/Malformed Request Missing Key: {error}")

        # NOTE: Storing UserData
        self.people.append(Person(name=name, email=email, image=body.get("image", b'')))

        # NOTE: Json Response
        return JSONResponse({"message": "User Was Created"})

    @route_fn(path="/list", methods=["GET"], context=context)
    async def list_people(self, request: Annotated[Request, "Request Data"]) -> StreamingResponse:
        """
        summary: Get A List Of Created People
        description: |
            # List Users
            Asynchronously List Users In a Json Format. Returning all details
            about every user lazily loading them in order of newest to oldest
            entry.
        responses:
            200:
                description: List Of Users
                content:
                    application/json:
                        schema:
                            type: list
                            description: |
                                # Users
                                List of users
                            items:
                                type: object
                                required:
                                    - "name"
                                    - "email"
                                properties:
                                    name:
                                        type: string
                                        description: |
                                            # Name
                                            This is the name of the user/client
                                    email:
                                        type: string
                                        description: |
                                            # Email
                                            This is the email of the user/client
                                    image:
                                        type: string
                                        description: |
                                            # Image
                                            This is a optional link for a image

        """
        # NOTE: Async Response
        return StreamingResponse(self.people_json(), media_type="application/json")

    @route_fn(path="/", methods=["GET"], context=context, include_in_schema=False)
    async def list_people_html(self, request: Annotated[Request, "Request Data"]) -> StreamingResponse:
        """
        summary: Html Page Of Created People
        description: |
            Returns A Html View Of All Users Asynchronously in order of newest
            to oldest entry.
        responses:
            200:
                description: List Of Users
        """
        # NOTE: Async Response
        return StreamingResponse(self.people_html(), media_type="text/html")


    async def people_json(self):
        """
        # Async Json Function
        Pushes each user as it is found on the people object in order of
        newest to oldest entry.
        """
        yield '['
        amount_of_people = len(self.people)
        for index, person in enumerate(reversed(self.people)):
            if (index + 1) != amount_of_people:
                yield '%s,' % person.json()
            else:
                yield '%s' % person.json()
        yield ']'

    async def people_html(self):
        """
        # Async HTML Template Function
        Pushes each user as it is found on the people object in order of
        newest to oldest entry.
        """
        yield """
        <html>
            <body>
                <h1 style="text-align: center">People Directory</h1>
                <div style="
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                ">
        """
        for person in reversed(self.people):
            yield f"""
            <div style=
                "border: 1px solid #ccc;
                border-radius: 16px;
                padding: 1rem;
                margin: 0.5rem"
            >
                <div style="display: flex; justify-content: space-evenly;">
                    {f'<img src="{person.image}" style="margin: 0.5rem; height: 3rem; width: 3rem; clip-path: circle()">' if person.image != '' else ''}
                    <h1 style="margin: 0.5 rem">{person.name}</h1>
                </div>
                <p style="margin: 0.5rem">
                        Email: <a href="mailto:{person.email}">{person.email}</a>
                </p>
            </div>
            """
        yield """
                </div>
            </body>
        </html>
        """

    @route_fn(path="/hello_name", methods=["GET"], context=context)
    async def hello_name(self, request: Annotated[Request, "Request Data"]) -> JSONResponse:
        """
        summary: "Test Route: Hello"
        description: |
            # Hello!!!

            Have you or someone you know ever wanted to say hello but cant.
            *Well this is the route for you. 👍*
        deprecated: true
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
                description: Returns Hello Response
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
            400:
                description: Request Malformed
                content:
                    text/plain:
                        schema:
                            type: string
                            default: "Bad/Malformed Request"
        """
        try:
            # NOTE: Could return a error if qurey pram not found
            return JSONResponse({
                "message": {"hello": request.query_params["name"]}
            })
        except KeyError as error: # NOTE: Catch possible Error
            raise HTTPException(status_code=400, detail=f"Bad/Malformed Request: {error}")
