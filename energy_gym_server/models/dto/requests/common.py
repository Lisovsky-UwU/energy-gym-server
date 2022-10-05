from typing import List, Optional
from pydantic import BaseModel, root_validator


class ItemsDeleteRequest(BaseModel):
    code: Optional[int]
    code_list: Optional[List[int]]

    @root_validator
    def required_field(cls, fields):
        if not (bool(fields.get("code")) ^ bool(fields.get("code_list"))):
            raise ValueError('Необходим один из параметров code или code_list')

        return fields


class ItemByCodeRequest(BaseModel):
    code: int


class ItemListByCodesRequest(BaseModel):
    code_list: List[int]
