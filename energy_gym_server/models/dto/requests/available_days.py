from typing import List
from pydantic import BaseModel
from datetime import date


class AvailableTimeAddRequest(BaseModel):
    weektime: str
    number_of_persons: int


class AvailableTimeListInPeriodRequest(BaseModel):
    date_begin: date
    date_end: date
