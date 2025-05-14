from typing import Annotated  # NOTE: Annotate Parameter Fields
# NOTE: BaseModel Is A Way To Describe A Custom Type
from pydantic import BaseModel


class Person(BaseModel):
    """
    Person Is A Data Class Or Type To Hold Data About A Person.
    """
    name: Annotated[str, "Name Of The User"]
    email: Annotated[str, "Email Of The User"]
    image: Annotated[str, "Image Link Or Base64 Encoded Image Optional"] = ""
