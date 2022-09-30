from tokenize import group
from typing import List
from sqlalchemy.future import select

from . import DataBaseService
from ..models import dto, database


class StudentsService(DataBaseService):

    async def add_student(self, request: dto.StudentAddRequest) -> dto.Student:
        student = database.Student(**request.dict())
        self.session.add(student)
        await self.session.flush()

        return dto.Student(
            code=student.code,
            name=student.name,
            group=student.group
        )


    async def get_student_list(self) -> dto.StudentList:
        return dto.StudentList(
            student_list=[
                dto.Student(
                    code=db_student.code,
                    name=db_student.name,
                    group=db_student.group
                )
                for db_student in (
                    await self.__get_student_list_for_filter__() 
                )
            ]
        )

    async def __get_student_list_for_filter__(self, filter: List = []) -> List[database.Student]:
        return list(
            await self.session.scalars(
                select(database.Student)
                .filter(*filter)
                .order_by(database.Student.code)
            )
        )
