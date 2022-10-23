from typing import List
from pydantic import BaseModel

from .. import AvailableTimeBase, AvailableTimeDetailed


class AvailableTimeBaseList(BaseModel):
    list: List[AvailableTimeBase]


class AvailableTimeDetailedList(BaseModel):
    list: List[AvailableTimeDetailed]
