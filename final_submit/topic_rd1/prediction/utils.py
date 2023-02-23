
# importing dependent libraries
from pydantic import BaseModel

# Input schema 
class Item(BaseModel):
    text: str
    model: str