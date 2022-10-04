from typing import List
from pydantic import BaseModel
from datetime import date


class AvailableDayAddRequest(BaseModel):
    day: date
    number_of_students: int


class AvailableDayListByCodeRequest(BaseModel):
    code_list: List[int]


class AvailableDayListInPeriodRequest(BaseModel):
    date_begin: date
    date_end: date


class AvailableDayByDateRequest(BaseModel):
    date: date
