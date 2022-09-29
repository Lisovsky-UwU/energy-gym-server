from typing import List
from pydantic import BaseModel

from .. import Entry


class EntryList(BaseModel):
    entries: List[Entry]
    