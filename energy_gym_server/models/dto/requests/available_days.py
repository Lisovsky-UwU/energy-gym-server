from datetime import date
from typing import List, Optional
from pydantic import BaseModel, root_validator


class AvailableDayAddRequest(BaseModel):
    day: date
    number_of_students: int


class AvailableDayByCodeRequest(BaseModel):
    code: int


class AvailableDayListByCodeRequest(BaseModel):
    code_list: List[int]


class AvailableDayListInPeriodRequest(BaseModel):
    date_begin: date
    date_end: date


class AvailableDayByDateRequest(BaseModel):
    date: date


class AvailableDayDeleteRequest(BaseModel):
    code: Optional[int]
    code_list: Optional[List[int]]

    @root_validator
    def required_field(cls, fields):
        if not (bool(fields.get("code")) ^ bool(fields.get("code_list"))):
            raise ValueError('Необходим один из параметров code или code_list')

        return fields
