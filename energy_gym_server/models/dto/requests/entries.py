from pydantic import BaseModel


class EntryAddRequest(BaseModel):
    selected_day: int
    user_code: int


class EntryListInDayRequest(BaseModel):
    available_day: int


class EntryListUserRequest(BaseModel):
    user_code: int
