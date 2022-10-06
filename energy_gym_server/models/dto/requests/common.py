from typing import List
from pydantic import BaseModel


class ItemDeleteRequest(BaseModel):
    code: int


class ItemByCodeRequest(BaseModel):
    code: int


class ItemListByCodesRequest(BaseModel):
    code_list: List[int]
