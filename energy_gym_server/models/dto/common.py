from pydantic import BaseModel
from datetime import date, datetime


class Student(BaseModel):
    code: int
    name: str
    group: str


class AvailableDayBase(BaseModel):
    code: int
    day: date
    number_of_student: int


class AvailableDayDetailed(AvailableDayBase):
    free_seats: int


class Entry(BaseModel):
    code: int
    create_time: datetime
    selected_day: date
    student_code: int
