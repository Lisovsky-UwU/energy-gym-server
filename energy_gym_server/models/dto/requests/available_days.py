from typing import List
from pydantic import BaseModel, Field
from datetime import date, datetime


def get_current_month():
    cur_time = datetime.now()
    return f'{cur_time.month}-{cur_time.year}'


class AvailableTimeAddRequest(BaseModel):
    weektime: str
    number_of_persons: int
    month: str = Field(default_factory=get_current_month)


class AvailableTimeListAddRequest(BaseModel):
    list: List[AvailableTimeAddRequest]


class AvailableTimeListInPeriodRequest(BaseModel):
    date_begin: date
    date_end: date
