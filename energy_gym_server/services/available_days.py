from typing import List
from sqlalchemy.future import select
from sqlalchemy import func

from .abc import BaseService
from ..models import dto, database
from ..exceptions import DataCorrectException


class AvailableDaysService(BaseService):

    async def add_day(self, request: dto.AvailableDayAddRequest) -> dto.AvailableDayBase:
        if await self.__get_one_item_for_filter__(database.AvailableDay, [database.AvailableDay.day == request.day]) is not None:
            raise DataCorrectException('Запись на данный день уже существует')

        available_day = database.AvailableDay(**request.dict())
        self.session.add(available_day)
        await self.session.flush()
        
        return dto.AvailableDayBase(
            code=available_day.code,
            day=available_day.day,
            number_of_students=available_day.number_of_students
        )

    async def get_all_days(self) -> dto.AvailableDayList:
        return await self.__get_days_with_free_seats__(
            await self.__get_item_list_for_filter__(database.AvailableDay)
        )


    async def get_days_by_period(self, request: dto.AvailableDayListInPeriodRequest) -> dto.AvailableDayList:
        return await self.__get_days_with_free_seats__(
            await self.__get_item_list_for_filter__(
                database.AvailableDay,
                [
                    database.AvailableDay.day >= request.date_begin, 
                    database.AvailableDay.day <= request.date_end
                ]
            )
        )


    async def delete_day(self, request: dto.ItemsDeleteRequest) -> dto.ItemsDeleted:
        return await self.__delete_items__(database.AvailableDay, request)


    async def __get_days_with_free_seats__(self, db_day_list: List[database.AvailableDay]):
        result_list = []
        for db_day in db_day_list:
            entries_day = (
                await self.session.execute(
                    select(func.count())
                    .select_from(
                        select(database.Entry)
                        .filter(database.Entry.selected_day == db_day.code)
                        .subquery()
                    )
                )
            ).one()
            result_list.append(
                dto.AvailableDayDetailed
                (
                    code=db_day.code,
                    day=db_day.day,
                    number_of_students=db_day.number_of_students,
                    free_seats=db_day.number_of_students - entries_day.count
                )
            )
        
        return dto.AvailableDayList(
            day_list=result_list
        )
