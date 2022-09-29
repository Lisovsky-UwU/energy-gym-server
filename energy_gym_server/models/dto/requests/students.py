from pydantic import BaseModel

from .. import Student


class StudentByCodeRequest(BaseModel):
    code: int


class AddStudentRequest(Student):
    pass
