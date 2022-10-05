from datetime import datetime
from typing import List
from sqlalchemy import select, func, any_

from .abc import BaseService
from ..models import dto, database
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class EntriesService(BaseService):
    
    async def get_list_all_entry(self) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__()


    async def get_entries_in_day(self, request: dto.EntryListInDayRequest) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.selected_day == request.available_day
            ]
        )

    
    async def get_entries_for_student(self, request: dto.EntryListStudentRequest) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.student == request.student_code
            ]
        )


    async def get_detailed_entry(self, request: dto.ItemByCodeRequest) -> dto.EntryDetailed:
        db_entry = await self.__get_one_item_for_filter__(database.Entry, [database.Entry.code == request.code])
        if db_entry is None:
            raise GetDataCorrectException('Запрашиваемая запись не найдена')
        
        return await self.__get_detailed_entry__(db_entry)

    
    async def get_entry_list_by_codes(self, request: dto.ItemListByCodesRequest) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.code == any_(request.code_list)
            ]
        )


    async def add_entry(self, request: dto.EntryAddRequest) -> dto.EntryModel:
        db_selected_day = await self.__get_one_item_for_filter__(database.AvailableDay, [database.AvailableDay.code == request.selected_day])
        if db_selected_day is None:
            raise AddDataCorrectException('На указанный день возможные записи отсутствуют')
        if await self.__get_one_item_for_filter__(database.Student, [database.Student.code == request.student_code]) is None:
            raise GetDataCorrectException('Указанный студент не найден')

        if await self.__get_one_item_for_filter__(database.Entry, [
                database.Entry.student == request.student_code,
                database.Entry.selected_day == request.selected_day
            ]) is not None:
            raise AddDataCorrectException('Такая запись уже существует')

        entries_day = (
            await self.session.execute(
                select(func.count())
                .select_from(
                    select(database.Entry)
                    .filter(database.Entry.selected_day == request.selected_day)
                    .subquery()
                )
            )
        ).one()

        if db_selected_day.number_of_students - entries_day.count <= 0:
            raise AddDataCorrectException('На данный день отсутствуют свободные места')

        entry = database.Entry(
            create_time=datetime.now(),
            selected_day=request.selected_day,
            student=request.student_code
        )
        self.session.add(entry)
        
        await self.session.flush()

        return dto.EntryModel(
            code=entry.code,
            create_time=entry.create_time,
            selected_day=entry.selected_day,
            student=entry.student
        )


    async def delete_entry(self, request: dto.ItemsDeleteRequest) -> dto.ItemsDeleted:
        return await self.__delete_items__(database.Entry, request)


    async def __get_detailed_entry__(self, db_entry: database.Entry) -> dto.EntryDetailed:
        db_selected_day = await self.__get_one_item_for_filter__(
            database.AvailableDay, 
            [
                database.AvailableDay.code == db_entry.selected_day
            ]
        )
        db_student = await self.__get_one_item_for_filter__(
            database.Student, 
            [
                database.Student.code == db_entry.student
            ]
        )

        return dto.EntryDetailed(
            code=db_entry.code,
            create_time=db_entry.create_time,
            selected_day=db_selected_day.__dict__,
            student=db_student.__dict__
        )


    async def __get_entry_list_for_filter__(self, filter: List = []) -> dto.EntryList:
        return dto.EntryList(
            entry_list=[
                dto.EntryModel(
                    **db_entry.__dict__
                )
                for db_entry in (
                    await self.__get_item_list_for_filter__(database.Entry, filter)
                )
            ]
        )
