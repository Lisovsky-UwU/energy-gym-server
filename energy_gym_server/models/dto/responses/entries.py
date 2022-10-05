from datetime import datetime
from typing import List
from pydantic import BaseModel

from .. import EntryModel, AvailableDayBase, StudentModel


class EntryList(BaseModel):
    entry_list: List[EntryModel]


class EntryDetailed(BaseModel):
    code: int
    create_time: datetime
    selected_day: AvailableDayBase
    student: StudentModel
