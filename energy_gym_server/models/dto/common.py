from typing import List
from pydantic import BaseModel
from datetime import date, datetime


class UserModel(BaseModel):
    code: int
    name: str
    group: str


class AvailableTimeBase(BaseModel):
    code: int
    weektime: str
    number_of_persons: int


class AvailableTimeDetailed(AvailableTimeBase):
    free_seats: int
    month: str


class EntryModel(BaseModel):
    code: int
    create_time: datetime
    selected_day: int
    user: int


class TokenModel(BaseModel):
    token: str
    user: int
