from pydantic import BaseModel


class EntryAddRequest(BaseModel):
    selected_time: int
    user_code: int


class EntryListInTimeRequest(BaseModel):
    available_time: int


class EntryListUserRequest(BaseModel):
    user_code: int
