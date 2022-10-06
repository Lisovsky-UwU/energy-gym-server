from sqlalchemy.future import select
from sqlalchemy.sql import any_

from .abc import AsyncBaseService
from ..models import dto, database, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class StudentsService(AsyncBaseService):

    async def get_student_list(self) -> dto.StudentList:
        return dto.StudentList(
            student_list=[
                dto.StudentModel(
                    code=db_student.code,
                    name=db_student.name,
                    group=db_student.group
                )
                for db_student in (
                    await self.session.scalars(select(database.Student))
                )
            ]
        )
    

    async def get_by_code(self, request: dto.ItemByCodeRequest) -> dto.StudentModel:
        student = await self.session.get(database.Student, request.code)
        if student is None:
            raise GetDataCorrectException('Студент с запрашиваемым кодом не найден')

        return dto.StudentModel(
            code=student.code,
            name=student.name,
            group=student.group
        )


    async def get_list_by_codes(self, request: dto.ItemListByCodesRequest) -> dto.StudentList:
        return dto.StudentList(
            student_list=[
                dto.StudentModel(
                    code=db_student.code,
                    name=db_student.name,
                    group=db_student.group
                )
                for db_student in (
                    await self.session.scalars(
                        select(database.Student)
                        .where(database.Student.code == any_(request.code_list))
                    )
                )
            ]
        )


    async def add_student(self, request: dto.RegistrationStudentRequest) -> dto.StudentModel:
        if await self.session.get(database.Student, request.code) is not None:
            raise AddDataCorrectException('Студент с данным идентефикатором уже существует')

        student = database.Student(
            **request.dict(),
            role=UserRoles.STUDENT.name
        )
        self.session.add(student)
        await self.session.flush()

        return dto.StudentModel(
            code=student.code,
            name=student.name,
            group=student.group
        )


    async def delete_student(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        await self.session.delete(
            self.session.get(database.Student, request.code)
        )
        return dto.ItemsDeleted(
            result_text='Студент успешно удален'
        )
