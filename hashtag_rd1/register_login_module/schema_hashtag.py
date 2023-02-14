from pydantic import BaseModel, constr, ValidationError


class AuthDetails(BaseModel):
    username: constr(min_length=6, max_length=15)
    password: constr(min_length=8, max_length=15)


class Item(BaseModel):
    text: str
    model: str
