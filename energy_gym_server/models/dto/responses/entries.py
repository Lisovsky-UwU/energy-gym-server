from datetime import datetime
from typing import List
from pydantic import BaseModel

from .. import EntryModel, AvailableDayBase, Student


class EntryList(BaseModel):
    entry_list: List[EntryModel]


class DetailedEntry(BaseModel):
    code: int
    create_time: datetime
    selected_day: AvailableDayBase
    student: Student
