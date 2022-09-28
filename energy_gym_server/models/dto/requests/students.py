from pydantic import BaseModel

from .. import Student


class StudentByCode(BaseModel):
    code: int


class AddStudent(Student):
    pass
