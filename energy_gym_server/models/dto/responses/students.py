from typing import List
from pydantic import BaseModel

from .. import Student


class StudentList(BaseModel):
    student_list: List[Student]
