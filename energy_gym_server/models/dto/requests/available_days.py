from datetime import date
from typing import List
from pydantic import BaseModel


class AvailableDayAddRequest(BaseModel):
    day: date
    number_of_students: int


class AvailableDayByCodeRequest(BaseModel):
    code: int


class AvailableDaysByCodeRequest(BaseModel):
    codes: List[int]


class AvailableDaysInPeriodRequest(BaseModel):
    date_begin: date
    date_end: date


class AvailableDayByDateRequest(BaseModel):
    date: date
