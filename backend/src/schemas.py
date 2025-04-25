from typing import List

from pydantic import BaseModel
from .models import Item

class ItemResponse(Item):
    id: str

class ItemsResponse(BaseModel):
    items: List[ItemResponse]