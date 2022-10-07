from typing import List
from sqlalchemy.future import select
from sqlalchemy.sql import func, any_

from .abc import AsyncBaseService
from ..models import dto, database
from ..exceptions import AddDataCorrectException, GetDataCorrectException


class AvailableDaysService(AsyncBaseService):

    async def get_all_days(self) -> dto.AvailableDayList:
        return await self.__get_day_list_with_free_seats__(
            await self.session.scalars(
                select(database.AvailableDay)
            )
        )


    async def get_days_by_period(self, request: dto.AvailableDayListInPeriodRequest) -> dto.AvailableDayList:
        return await self.__get_day_list_with_free_seats__(
            await self.session.scalars(
                select(database.AvailableDay)
                .where(database.AvailableDay.day >= request.date_begin)
                .where(database.AvailableDay.day <= request.date_end)
            )
        )


    async def get_day_by_code(self, request: dto.ItemByCodeRequest) -> dto.AvailableDayDetailed:
        available_day = await self.session.get(database.AvailableDay, request.code)
        if available_day is None:
            raise GetDataCorrectException('Запрашиваемый день не найден')

        return await self.__get_day_with_free_seats__(available_day)


    async def get_day_list_by_codes(self, request: dto.ItemListByCodesRequest) -> dto.AvailableDayList:
        return await self.__get_day_list_with_free_seats__(
            await self.session.scalars(
                select(database.AvailableDay)
                .where(database.AvailableDay.code == any_(request.code_list))
            )
        )


    async def add_day(self, request: dto.AvailableDayAddRequest) -> dto.AvailableDayBase:
        if await self.session.scalar(
            select(database.AvailableDay)
            .where(database.AvailableDay.day == request.day)
        ) is not None:
            raise AddDataCorrectException('Запись на данный день уже существует')

        available_day = database.AvailableDay(**request.dict())
        self.session.add(available_day)
        await self.session.flush()
        
        return dto.AvailableDayBase(
            code=available_day.code,
            day=available_day.day,
            number_of_persons=available_day.number_of_persons
        )


    async def delete_day(self, request: dto.ItemDeleteRequest) -> dto.ItemsDeleted:
        for db_entry in (
            await self.session.scalars(
                select(database.Entry)
                .where(database.Entry.selected_day == request.code)
            )
        ):
            await self.session.delete(db_entry)
        
        await self.session.delete(
            await self.session.get(database.AvailableDay, request.code)
        )
        return dto.ItemsDeleted(
            result_text='День для записи успешно удален'
        )


    async def __get_day_list_with_free_seats__(self, db_day_list: List[database.AvailableDay]) -> dto.AvailableDayList:
        result_list = []
        for db_day in db_day_list:
            result_list.append(await self.__get_day_with_free_seats__(db_day))
        
        return dto.AvailableDayList(
            day_list=result_list
        )

    
    async def __get_day_with_free_seats__(self, db_day: database.AvailableDay) -> dto.AvailableDayDetailed:
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
        return dto.AvailableDayDetailed(
            code=db_day.code,
            day=db_day.day,
            number_of_persons=db_day.number_of_persons,
            free_seats=db_day.number_of_persons - entries_day.count
        )
        