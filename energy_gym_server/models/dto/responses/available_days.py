from typing import List
from pydantic import BaseModel

from .. import AvailableDayDetailed


class AvailableDayList(BaseModel):
    day_list: List[AvailableDayDetailed]
