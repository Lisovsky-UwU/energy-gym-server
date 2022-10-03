from datetime import datetime
from typing import List
from sqlalchemy import any_
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from .abc import BaseService
from ..models import dto, database
from ..exceptions import DataCorrectException


class EntriesService(BaseService):
    
    async def add_entry(self, request: dto.AddEntryRequest) -> dto.EntryModel:
        if (await self.__get_one_item_for_filter__(database.AvailableDay, [database.AvailableDay.code == request.selected_day]) is None):
            raise DataCorrectException('На указанный день возможные записи отсутствуют')
        if (await self.__get_one_item_for_filter__(database.Student, [database.Student.code == request.student_code]) is None):
            raise DataCorrectException('Указанный студент не найден')

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


    async def get_list_all_entry(self) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__()


    async def delete_entry(self, request: dto.ItemsDeleteRequest) -> dto.ItemsDeleted:
        return await self.__delete_items__(database.Entry, request)


    async def get_entries_in_day(self, request: dto.EntriesInDayRequest) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.selected_day == request.available_day
            ]
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
