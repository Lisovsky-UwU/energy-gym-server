from pydantic import BaseModel
from datetime import date, datetime


class Student(BaseModel):
    code: int
    name: str
    group: str


class AvailableDayBase(BaseModel):
    code: int
    day: date
    number_of_students: int


class AvailableDayDetailed(AvailableDayBase):
    free_seats: int


class EntryModel(BaseModel):
    code: int
    create_time: datetime
    selected_day: int
    student: int
