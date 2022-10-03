from typing import List
from pydantic import BaseModel

from .. import EntryModel


class EntryList(BaseModel):
    entry_list: List[EntryModel]
