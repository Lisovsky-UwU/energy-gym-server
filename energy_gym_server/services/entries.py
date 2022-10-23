from datetime import datetime
from typing import List
from sqlalchemy.sql import func, any_
from sqlalchemy.future import select

from .abc import BaseService
from ..models import dto, database, AccesRights, UserRoles
from ..exceptions import AddDataCorrectException, GetDataCorrectException, AccessRightsException


class EntriesService(BaseService):
    
    def get_list_all_entry(self) -> dto.EntryList:
        return self.__get_entry_list_for_filter__()


    def get_entries_in_time(self, request: dto.EntryListInTimeRequest) -> dto.EntryList:
        return self.__get_entry_list_for_filter__(
            [
                database.Entry.selected_time == request.available_time
            ]
        )

    
    def get_entries_for_user(self, db_user: database.User, request: dto.EntryListUserRequest) -> dto.EntryList:
        self.__check_access_for_user__(db_user, request.user_code)
        return self.__get_entry_list_for_filter__(
            [
                database.Entry.user == request.user_code
            ]
        )


    def get_detailed_entry(self, db_user: database.User, request: dto.ItemByCodeRequest) -> dto.EntryDetailed:
        self.__check_access_for_entry__(db_user, request.code)
        db_entry = self.session.get(database.Entry, request.code)
        if db_entry is None:
            raise GetDataCorrectException('Запрашиваемая запись не найдена')
        
        return self.__get_detailed_entry__(db_entry)


    def add_entry(self, db_user: database.User, request: dto.EntryAddRequest) -> dto.EntryModel:
        self.__check_access_for_user__(db_user, request.user_code)

        db_selected_time = self.session.get(database.AvailableTime, request.selected_time)
        if db_selected_time is None:
            raise AddDataCorrectException('На указанное время возможные записи отсутствуют')
        if self.session.get(database.User, request.user_code) is None:
            raise GetDataCorrectException('Указанный студент не найден')

        if self.session.scalar(
            select(database.Entry)
            .where(database.Entry.user == request.user_code)
            .where(database.Entry.selected_time == request.selected_time)
        ) is not None:
            raise AddDataCorrectException('Такая запись уже существует')

        entries_time = (
            self.session.execute(
                select(func.count())
                .select_from(
                    select(database.Entry)
                    .filter(database.Entry.selected_time == request.selected_time)
                    .subquery()
                )
            )
        ).one()

        if db_selected_time.number_of_persons - entries_time.count <= 0:
            raise AddDataCorrectException('На данное время отсутствуют свободные места')

        entry = database.Entry(
            create_time=datetime.now(),
            selected_time=request.selected_time,
            user=request.user_code
        )
        self.session.add(entry)
        
        self.session.flush()

        return dto.EntryModel(
            code=entry.code,
            create_time=entry.create_time,
            selected_time=entry.selected_time,
            user=entry.user
        )


    def delete_entry(self, db_user: database.User, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        self.__check_access_for_entry__(db_user, request.code)

        self.session.delete(
            self.session.get(database.Entry, request.code)
        )
        return dto.ItemsDeleted(
            result_text='Запись успешно удалена'
        )


    def __get_detailed_entry__(self, db_entry: database.Entry) -> dto.EntryDetailed:
        db_selected_time = self.session.get(database.AvailableTime, db_entry.selected_time)
        db_user = self.session.get(database.User, db_entry.user)

        return dto.EntryDetailed(
            code=db_entry.code,
            create_time=db_entry.create_time,
            selected_time=dto.AvailableTimeBase(
                code=db_selected_time.code,
                weektime=db_selected_time.weektime,
                number_of_persons=db_selected_time.number_of_persons
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
                    selected_time=db_entry.selected_time,
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


    def __check_access_for_entry__(self, db_user: database.User, entry_code: int):
        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value:
            db_entry: database.Entry = self.session.get(database.Entry, entry_code)
            if db_entry is None:
                raise GetDataCorrectException('Запрашиваемая запись не найдена')

            if db_entry.user != db_user.code:
                raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')


    def __check_access_for_user__(self, db_user: database.User, access_user_code: int):
        if AccesRights.ENTRY.EDITANY not in UserRoles[db_user.role].value and db_user.code != access_user_code:
            raise AccessRightsException('Для выполнения данной операции у вас недостаточно прав')
