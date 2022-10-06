import asyncio
from typing import TypeVar, List
from sqlalchemy.orm import Session
from sqlalchemy.sql import any_
from sqlalchemy.future import select

from ..exceptions import DataBaseConnectionException
from ..models import dto
from ..models.database import session_factory


class AsyncDataBaseService:
    
    def __init__(self, session: Session = None, **kwargs):
        if session is None:
            self.session = session_factory(**kwargs)
        else:
            self.session = session

    def __getattr__(self, attr):
        return getattr(self.session, attr)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()

        if exc_type is not None:
            if issubclass(exc_type, ConnectionError):
                raise DataBaseConnectionException("Отсутствует соединение с базой данных")


T = TypeVar('T')

class BaseService(AsyncDataBaseService):

    async def __delete_items__(self, type_table: T, request: dto.ItemsDeleteRequest):
        code_list_for_delete = []
        if request.code is not None:
            code_list_for_delete.append(request.code)
        if request.code_list is not None:
            code_list_for_delete = request.code_list

        await self.__delete_items_by_codes__(type_table, code_list_for_delete)

        return dto.ItemsDeleted(
            result_text=f'Записи с кодами {code_list_for_delete} успешно удалены'
        )


    async def __delete_items_by_codes__(self, type_table: T, code_list: List[int]) -> None:
        db_item_list = await self.session.scalar(
            select(type_table)
            .where(type_table.code == any_(code_list))
        )
        
        delete_task_list = []
        for db_item in db_item_list:
            delete_task_list.append(self.session.delete(db_item))
        
        await asyncio.gather(*delete_task_list)
