from typing import List, Optional
from datetime import date
from pydantic import BaseModel, root_validator


class AddEntryRequest(BaseModel):
    selected_day: int
    student_code: int


class EntryByCodeRequest(BaseModel):
    code: int


class DayEntriesRequest(BaseModel):
    date: date


class StudentEntriesRequest(BaseModel):
    student_code: int


class EntryDeleteRequest(BaseModel):
    code: Optional[int]
    code_list: Optional[List[int]]

    @root_validator
    def required_field(cls, fields):
        if not (bool(fields.get("code")) ^ bool(fields.get("code_list"))):
            raise ValueError('Необходим один из параметров code или code_list')

        return fields
