from typing import List
from pydantic import BaseModel

from .. import AvailableTimeDetailed


class AvailableTimeList(BaseModel):
    time_list: List[AvailableTimeDetailed]
