from typing import List
from pydantic import BaseModel

from .. import AvailableDayDetailed


class AllDays(BaseModel):
    day_list: List[AvailableDayDetailed]
