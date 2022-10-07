from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class UserModel(BaseModel):
    code: int
    name: str
    group: str


class AvailableDayBase(BaseModel):
    code: int
    day: date
    number_of_persons: int


class AvailableDayDetailed(AvailableDayBase):
    free_seats: int


class EntryModel(BaseModel):
    code: int
    create_time: datetime
    selected_day: int
    user: int


class TokenModel(BaseModel):
    token: str
    user: int
