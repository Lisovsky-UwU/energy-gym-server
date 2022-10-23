from typing import List
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.sql import func, any_

from .abc import BaseService
from ..models import dto, database
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class AvailableTimeService(BaseService):

    def get_all_time(self, all_months: bool = False) -> dto.AvailableTimeDetailedList:
        cur_time = datetime.now()
        return self.__get_time_list_with_free_seats__(
            self.session.scalars(
                select(database.AvailableTime)
                .where(database.AvailableTime.month == f'{cur_time.month}-{cur_time.year}' if all_months == False else True)
            )
        )


    # def get_days_by_period(self, request: dto.AvailableDayListInPeriodRequest) -> dto.AvailableTimeList:
    #     return self.__get_day_list_with_free_seats__(
    #         self.session.scalars(
    #             select(database.AvailableTime)
    #             .where(database.AvailableTime.weektime >= request.date_begin)
    #             .where(database.AvailableTime.weektime <= request.date_end)
    #         )
    #     )


    def get_time_by_code(self, request: dto.ItemByCodeRequest) -> dto.AvailableTimeDetailed:
        available_time = self.session.get(database.AvailableTime, request.code)
        if available_time is None:
            raise GetDataCorrectException('Запрашиваемое время не найдено')

        return self.__get_time_with_free_seats__(available_time)


    def add_time(self, request: dto.AvailableTimeAddRequest) -> dto.AvailableTimeBase:
        if self.session.scalar(
            select(database.AvailableTime)
            .where(database.AvailableTime.weektime == request.weektime)
            .where(database.AvailableTime.month == request.month)
        ) is not None:
            raise AddDataCorrectException('Запись на данное время уже существует')

        available_time = database.AvailableTime(**request.dict())
        self.session.add(available_time)
        self.session.flush()
        
        return dto.AvailableTimeBase(
            code=available_time.code,
            weektime=available_time.weektime,
            number_of_persons=available_time.number_of_persons
        )


    def add_time_from_list(self, request: dto.AvailableTimeListAddRequest) -> dto.AvailableTimeBaseList:
        result_list = []
        for added_time in request.list:
            try:
                result_list.append(self.add_time(added_time))
            except AddDataCorrectException:
                pass
        
        return dto.AvailableTimeBaseList(list=result_list)


    def delete_time(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        for db_entry in (
            self.session.scalars(
                select(database.Entry)
                .where(database.Entry.selected_time == request.code)
            )
        ):
            self.session.delete(db_entry)
        
        self.session.delete(
            self.session.get(database.AvailableTime, request.code)
        )
        return dto.ItemsDeleted(
            result_text='Время для записи успешно удалено'
        )


    def __get_time_list_with_free_seats__(self, db_time_list: List[database.AvailableTime]) -> dto.AvailableTimeDetailedList:
        result_list = []
        for db_time in db_time_list:
            result_list.append(self.__get_time_with_free_seats__(db_time))
        
        return dto.AvailableTimeDetailedList(
            list=result_list
        )

    
    def __get_time_with_free_seats__(self, db_time: database.AvailableTime) -> dto.AvailableTimeDetailed:
        entries_time = (
            self.session.execute(
                select(func.count())
                .select_from(
                    select(database.Entry)
                    .filter(database.Entry.selected_time == db_time.code)
                    .subquery()
                )
            )
        ).one()
        return dto.AvailableTimeDetailed(
            code=db_time.code,
            weektime=db_time.weektime,
            number_of_persons=db_time.number_of_persons,
            free_seats=db_time.number_of_persons - entries_time.count,
            month=db_time.month
        )
        