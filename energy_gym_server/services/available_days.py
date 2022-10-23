from typing import List
from sqlalchemy.future import select
from sqlalchemy.sql import func, any_

from .abc import BaseService
from ..models import dto, database
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class AvailableDaysService(BaseService):

    def get_all_days(self) -> dto.AvailableDayList:
        return self.__get_day_list_with_free_seats__(
            self.session.scalars(
                select(database.AvailableDay)
            )
        )


    def get_days_by_period(self, request: dto.AvailableDayListInPeriodRequest) -> dto.AvailableDayList:
        return self.__get_day_list_with_free_seats__(
            self.session.scalars(
                select(database.AvailableDay)
                .where(database.AvailableDay.day >= request.date_begin)
                .where(database.AvailableDay.day <= request.date_end)
            )
        )


    def get_day_by_code(self, request: dto.ItemByCodeRequest) -> dto.AvailableDayDetailed:
        available_day = self.session.get(database.AvailableDay, request.code)
        if available_day is None:
            raise GetDataCorrectException('Запрашиваемый день не найден')

        return self.__get_day_with_free_seats__(available_day)


    def add_day(self, request: dto.AvailableDayAddRequest) -> dto.AvailableDayBase:
        if self.session.scalar(
            select(database.AvailableDay)
            .where(database.AvailableDay.day == request.day)
        ) is not None:
            raise AddDataCorrectException('Запись на данный день уже существует')

        available_day = database.AvailableDay(**request.dict())
        self.session.add(available_day)
        self.session.flush()
        
        return dto.AvailableDayBase(
            code=available_day.code,
            day=available_day.day,
            number_of_persons=available_day.number_of_persons
        )


    def delete_day(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        for db_entry in (
            self.session.scalars(
                select(database.Entry)
                .where(database.Entry.selected_day == request.code)
            )
        ):
            self.session.delete(db_entry)
        
        self.session.delete(
            self.session.get(database.AvailableDay, request.code)
        )
        return dto.ItemsDeleted(
            result_text='День для записи успешно удален'
        )


    def __get_day_list_with_free_seats__(self, db_day_list: List[database.AvailableDay]) -> dto.AvailableDayList:
        result_list = []
        for db_day in db_day_list:
            result_list.append(self.__get_day_with_free_seats__(db_day))
        
        return dto.AvailableDayList(
            day_list=result_list
        )

    
    def __get_day_with_free_seats__(self, db_day: database.AvailableDay) -> dto.AvailableDayDetailed:
        entries_day = (
            self.session.execute(
                select(func.count())
                .select_from(
                    select(database.Entry)
                    .filter(database.Entry.selected_day == db_day.code)
                    .subquery()
                )
            )
        ).one()
        return dto.AvailableDayDetailed(
            code=db_day.code,
            day=db_day.day,
            number_of_persons=db_day.number_of_persons,
            free_seats=db_day.number_of_persons - entries_day.count
        )
        