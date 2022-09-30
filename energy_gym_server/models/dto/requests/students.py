from pydantic import BaseModel

from .. import Student


class StudentAddRequest(Student):
    pass


class StudentByCodeRequest(BaseModel):
    code: int


class StudentAddRequest(Student):
    pass
