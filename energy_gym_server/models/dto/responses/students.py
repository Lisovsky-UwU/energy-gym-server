from typing import List
from pydantic import BaseModel

from .. import StudentModel


class StudentList(BaseModel):
    student_list: List[StudentModel]
