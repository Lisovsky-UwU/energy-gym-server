from datetime import datetime
from typing import List
from sqlalchemy import any_
from sqlalchemy.future import select

from . import DataBaseService
from ..models import dto, database


class EntriesService(DataBaseService):
    
    async def add_entry(self, request: dto.AddEntryRequest) -> dto.EntryModel:
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
            student_code=entry.student
        )


    async def get_list(self) -> dto.EntryList:
        return dto.EntryList(
            entry_list=[
                dto.EntryModel(
                    code=db_entry.code,
                    create_time=db_entry.create_time,
                    selected_day=db_entry.selected_day,
                    student_code=db_entry.student,
                )
                for db_entry in (
                    await self.__get_entry_list_for_filter__()
                )
            ]
        )


    async def delete_entry(self, request: dto.EntryDeleteRequest) -> dto.EntryDeleted:
        code_list_for_delete = []
        if request.code is not None:
            code_list_for_delete.append(request.code)
        if request.code_list is not None:
            code_list_for_delete = request.code_list

        db_entry_list = await self.__get_entry_list_for_filter__(
            [
                database.Entry.code == any_(code_list_for_delete)
            ]
        )
        
        for db_entry in db_entry_list:
            await self.session.delete(db_entry)

        return dto.StudentDeleted(
            result_text=f'Записи с кодами {code_list_for_delete} успешно удалены'
        )

    
    async def __get_entry_list_for_filter__(self, filter: List = [True]) -> List[database.Entry]:
        return list(
            await self.session.scalars(
                select(database.Entry)
                .filter(*filter)
                .order_by(database.Entry.code)
            )
        )
