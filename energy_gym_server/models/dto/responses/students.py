from typing import List
from pydantic import BaseModel

from .. import Student


class StudentList(BaseModel):
    stidents: List[Student]
