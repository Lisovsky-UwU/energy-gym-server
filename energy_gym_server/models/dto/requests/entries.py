from datetime import date
from pydantic import BaseModel


class CreateEntry(BaseModel):
    selected_day: date
    student_code: int


class EntryByCode(BaseModel):
    code: int


class DayEntries(BaseModel):
    date: date


class StudentEntries(BaseModel):
    student_code: int
