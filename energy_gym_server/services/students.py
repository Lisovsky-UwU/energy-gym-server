from typing import List
from sqlalchemy import any_
from sqlalchemy.future import select

from .abc import BaseService
from ..models import dto, database


class StudentsService(BaseService):

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
                    **db_student.__dict__
                )
                for db_student in (
                    await self.__get_item_list_for_filter__(database.Student) 
                )
            ]
        )


    async def delete_student(self, request: dto.ItemsDeleteRequest) -> dto.StudentDeleted:
        return await self.__delete_items__(database.Student, request)
