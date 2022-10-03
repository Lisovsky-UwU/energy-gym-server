from datetime import datetime
from typing import List
from sqlalchemy import any_
from sqlalchemy.future import select

from .abc import BaseService
from ..models import dto, database


class EntriesService(BaseService):
    
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
            student=entry.student
        )


    async def get_list(self) -> dto.EntryList:
        return dto.EntryList(
            entry_list=[
                dto.EntryModel(
                    **db_entry.__dict__
                )
                for db_entry in (
                    await self.__get_item_list_for_filter__(database.Entry)
                )
            ]
        )


    async def delete_entry(self, request: dto.ItemsDeleteRequest) -> dto.ItemsDeleted:
        return await self.__delete_items__(database.Entry, request)
