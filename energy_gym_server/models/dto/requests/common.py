from typing import List
from pydantic import BaseModel


class ItemDeleteRequest(BaseModel):
    code: int


class ItemByCodeRequest(BaseModel):
    code: int
