from datetime import datetime
from typing import List
from pydantic import BaseModel

from .. import EntryModel, AvailableDayBase, UserModel


class EntryList(BaseModel):
    entry_list: List[EntryModel]


class EntryDetailed(BaseModel):
    code: int
    create_time: datetime
    selected_day: AvailableDayBase
    user: UserModel
