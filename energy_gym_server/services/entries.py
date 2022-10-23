from datetime import datetime
from typing import List
from sqlalchemy.sql import func, any_
from sqlalchemy.future import select
from flask import request as flask_request

from .abc import BaseService
from ..models import dto, database, AccesRights, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException, AccessRightsException


class EntriesService(BaseService):
    
    def get_list_all_entry(self) -> dto.EntryList:
        return self.__get_entry_list_for_filter__()


    def get_entries_in_day(self, request: dto.EntryListInDayRequest) -> dto.EntryList:
        return self.__get_entry_list_for_filter__(
            [
                database.Entry.selected_time == request.available_day
            ]
        )

    
    def get_entries_for_user(self, request: dto.EntryListUserRequest) -> dto.EntryList:
        self.__check_access_for_user__(int(flask_request.headers.get('user_code')), request.user_code)
        return self.__get_entry_list_for_filter__(
            [
                database.Entry.user == request.user_code
            ]
        )


    def get_detailed_entry(self, request: dto.ItemByCodeRequest) -> dto.EntryDetailed:
        self.__check_access_for_entry__(int(flask_request.headers.get('user_code')), request.code)
        db_entry = self.session.get(database.Entry, request.code)
        if db_entry is None:
            raise GetDataCorrectException('Запрашиваемая запись не найдена')
        
        return self.__get_detailed_entry__(db_entry)


    def add_entry(self, request: dto.EntryAddRequest) -> dto.EntryModel:
        self.__check_access_for_user__(int(flask_request.headers.get('user_code')), request.user_code)

        db_selected_day = self.session.get(database.AvailableTime, request.selected_day)
        if db_selected_day is None:
            raise AddDataCorrectException('На указанный день возможные записи отсутствуют')
        if self.session.get(database.User, request.user_code) is None:
            raise GetDataCorrectException('Указанный студент не найден')

        if self.session.scalar(
            select(database.Entry)
            .where(database.Entry.user == request.user_code)
            .where(database.Entry.selected_time == request.selected_day)
        ) is not None:
            raise AddDataCorrectException('Такая запись уже существует')

        entries_day = (
            self.session.execute(
                select(func.count())
                .select_from(
                    select(database.Entry)
                    .filter(database.Entry.selected_time == request.selected_day)
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
        
        self.session.flush()

        return dto.EntryModel(
            code=entry.code,
            create_time=entry.create_time,
            selected_day=entry.selected_time,
            user=entry.user
        )


    def delete_entry(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        self.__check_access_for_entry__(int(flask_request.headers.get('user_code')), request.code)

        self.session.delete(
            self.session.get(database.Entry, request.code)
        )
        return dto.ItemsDeleted(
            result_text='Запись успешно удалена'
        )


    def __get_detailed_entry__(self, db_entry: database.Entry) -> dto.EntryDetailed:
        db_selected_day = self.session.get(database.AvailableTime, db_entry.selected_time)
        db_user = self.session.get(database.User, db_entry.user)

        return dto.EntryDetailed(
            code=db_entry.code,
            create_time=db_entry.create_time,
            selected_day=dto.AvailableTimeBase(
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


    def __get_entry_list_for_filter__(self, filter_: List = []) -> dto.EntryList:
        return dto.EntryList(
            entry_list=[
                dto.EntryModel(
                    code=db_entry.code,
                    create_time=db_entry.create_time,
                    selected_day=db_entry.selected_day,
                    user=db_entry.user
                )
                for db_entry in (
                    self.session.scalars(
                        select(database.Entry)
                        .filter(*filter_)
                    )
                )
            ]
        )


    def __check_access_for_entry__(self, user_code: int, entry_code: int):
        db_user: database.User = self.session.get(database.User, user_code)

        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value:
            db_entry: database.Entry = self.session.get(database.Entry, entry_code)
            if db_entry is None:
                raise GetDataCorrectException('Запрашиваемая запись не найдена')

            if db_entry.user != db_user.code:
                raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')


    def __check_access_for_user__(self, user_code: int, access_user_code: int):
        db_user: database.User = self.session.get(database.User, user_code)

        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value and db_user.code != access_user_code:
            raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
