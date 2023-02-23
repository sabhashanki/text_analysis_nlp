
# Importing dependent libraries
from pydantic import BaseModel, conlist

# Input schema
class Item(BaseModel):
    data: str
    labels: conlist(str, min_items=2, max_items=20)
    model: str