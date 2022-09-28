from datetime import date
from typing import List
from pydantic import BaseModel


class DayByCodeRequest(BaseModel):
    code: int


class DaysByCodeRequest(BaseModel):
    codes: List[int]


class PeriodDaysRequest(BaseModel):
    date_begin: date
    date_end: date


class DayByDate(BaseModel):
    date: date
