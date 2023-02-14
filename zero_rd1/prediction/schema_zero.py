from pydantic import BaseModel, constr, conlist


class AuthDetails(BaseModel):
    username: constr(min_length=6, max_length=15)
    password: constr(min_length=8, max_length=15)


class Item(BaseModel):
    data: str
    labels: conlist(str, min_items=2, max_items=20)
    model: str
