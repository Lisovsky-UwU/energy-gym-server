from pydantic import BaseModel


class EntryAddRequest(BaseModel):
    selected_day: int
    student_code: int


class EntryListInDayRequest(BaseModel):
    available_day: int


class EntryListStudentRequest(BaseModel):
    student_code: int
