from datetime import datetime
from typing import List
from sqlalchemy.sql import func, any_
from sqlalchemy.future import select
from quart import request as quart_request

from .abc import AsyncBaseService
from ..models import dto, database, AccesRights, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException, AccessRightsException


class EntriesService(AsyncBaseService):
    
    async def get_list_all_entry(self) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__()


    async def get_entries_in_day(self, request: dto.EntryListInDayRequest) -> dto.EntryList:
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.selected_day == request.available_day
            ]
        )

    
    async def get_entries_for_user(self, request: dto.EntryListUserRequest) -> dto.EntryList:
        await self.__check_access_for_user__(int(quart_request.headers.get('user_code')), request.user_code)
        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.user == request.user_code
            ]
        )


    async def get_detailed_entry(self, request: dto.ItemByCodeRequest) -> dto.EntryDetailed:
        await self.__check_access_for_entry__(int(quart_request.headers.get('user_code')), request.code)
        db_entry = await self.session.get(database.Entry, request.code)
        if db_entry is None:
            raise GetDataCorrectException('Запрашиваемая запись не найдена')
        
        return await self.__get_detailed_entry__(db_entry)

    
    async def get_entry_list_by_codes(self, request: dto.ItemListByCodesRequest) -> dto.EntryList:
        user_code = int(quart_request.headers.get('user_code'))
        for entry_code in request.code_list:
            await self.__check_access_for_entry__(user_code, entry_code)

        return await self.__get_entry_list_for_filter__(
            [
                database.Entry.code == any_(request.code_list)
            ]
        )


    async def add_entry(self, request: dto.EntryAddRequest) -> dto.EntryModel:
        await self.__check_access_for_user__(int(quart_request.headers.get('user_code')), request.user_code)

        db_selected_day = await self.session.get(database.AvailableDay, request.selected_day)
        if db_selected_day is None:
            raise AddDataCorrectException('На указанный день возможные записи отсутствуют')
        if await self.session.get(database.User, request.user_code) is None:
            raise GetDataCorrectException('Указанный студент не найден')

        if await self.session.scalar(
            select(database.Entry)
            .where(database.Entry.user == request.user_code)
            .where(database.Entry.selected_day == request.selected_day)
        ) is not None:
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

        if db_selected_day.number_of_persons - entries_day.count <= 0:
            raise AddDataCorrectException('На данный день отсутствуют свободные места')

        entry = database.Entry(
            create_time=datetime.now(),
            selected_day=request.selected_day,
            user=request.user_code
        )
        self.session.add(entry)
        
        await self.session.flush()

        return dto.EntryModel(
            code=entry.code,
            create_time=entry.create_time,
            selected_day=entry.selected_day,
            user=entry.user
        )


    async def delete_entry(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        await self.__check_access_for_entry__(int(quart_request.headers.get('user_code')), request.code)

        await self.session.delete(
            await self.session.get(database.Entry, request.code)
        )
        return dto.ItemsDeleted(
            result_text='Запись успешно удалена'
        )


    async def __get_detailed_entry__(self, db_entry: database.Entry) -> dto.EntryDetailed:
        db_selected_day = await self.session.get(database.AvailableDay, db_entry.selected_day)
        db_user = await self.session.get(database.User, db_entry.user)

        return dto.EntryDetailed(
            code=db_entry.code,
            create_time=db_entry.create_time,
            selected_day=dto.AvailableDayBase(
                code=db_selected_day.code,
                day=db_selected_day.day,
                number_of_persons=db_selected_day.number_of_persons
            ),
            user=dto.UserModel(
                code=db_user.code,
                name=db_user.name,
                group=db_user.group
            )
        )


    async def __get_entry_list_for_filter__(self, filter_: List = []) -> dto.EntryList:
        return dto.EntryList(
            entry_list=[
                dto.EntryModel(
                    code=db_entry.code,
                    create_time=db_entry.create_time,
                    selected_day=db_entry.selected_day,
                    user=db_entry.user
                )
                for db_entry in (
                    await self.session.scalars(
                        select(database.Entry)
                        .filter(*filter_)
                    )
                )
            ]
        )


    async def __check_access_for_entry__(self, user_code: int, entry_code: int):
        db_user: database.User = await self.session.get(database.User, user_code)

        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value:
            db_entry: database.Entry = await self.session.get(database.Entry, entry_code)
            if db_entry is None:
                raise GetDataCorrectException('Запрашиваемая запись не найдена')

            if db_entry.user != db_user.code:
                raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')


    async def __check_access_for_user__(self, user_code: int, access_user_code: int):
        db_user: database.User = await self.session.get(database.User, user_code)

        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value and db_user.code != access_user_code:
            raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
