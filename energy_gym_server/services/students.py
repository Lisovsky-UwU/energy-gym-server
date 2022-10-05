from .abc import BaseService
from ..models import dto, database
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class StudentsService(BaseService):

    async def add_student(self, request: dto.StudentAddRequest) -> dto.Student:
        if await self.__get_one_item_for_filter__(database.Student, [database.Student.code == request.code]) is not None:
            raise AddDataCorrectException('Студент с данным идентефикатором уже существует')

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

    
    async def get_by_code(self, request: dto.ItemByCodeRequest) -> dto.Student:
        student = await self.__get_one_item_for_filter__(
            database.Student, 
            [
                database.Student.code == request.code
            ]
        )
        if student is None:
            raise GetDataCorrectException('Студент с запрашиваемым кодом не найден')

        return dto.Student(**student.__dict__)


    async def delete_student(self, request: dto.ItemsDeleteRequest) -> dto.ItemsDeleted:
        return await self.__delete_items__(database.Student, request)
