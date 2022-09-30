from typing import List
from pydantic import BaseModel

from .. import AvailableDayDetailed


class AvailableDayList(BaseModel):
    day_list: List[AvailableDayDetailed]


class AvailableDayDeleted(BaseModel):
    result_text: str
