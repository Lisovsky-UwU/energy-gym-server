from pydantic import BaseModel


class AddEntryRequest(BaseModel):
    selected_day: int
    student_code: int


class EntriesInDayRequest(BaseModel):
    available_day: int


class StudentEntriesRequest(BaseModel):
    student_code: int
