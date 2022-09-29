from datetime import date
from pydantic import BaseModel


class CreateEntryRequest(BaseModel):
    selected_day: date
    student_code: int


class EntryByCodeRequest(BaseModel):
    code: int


class DayEntriesRequest(BaseModel):
    date: date


class StudentEntriesRequest(BaseModel):
    student_code: int
