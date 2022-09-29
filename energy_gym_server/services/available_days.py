from typing import List
from sqlalchemy.future import select
from sqlalchemy import func, cast, DATE

from . import DataBaseService
from ..models import dto, database


class AvailableDaysService(DataBaseService):

    async def add_day(self, request: dto.AvailableDayAddRequest) -> dto.AvailableDayBase:
        available_day = database.AvailableDay(
            day = request.day,
            number_of_students = request.number_of_students
        )
        self.session.add(available_day)
        await self.session.flush()
        
        return dto.AvailableDayBase(
            code=available_day.code,
            day=available_day.day,
            number_of_students=available_day.number_of_students
        )


    async def get_all_days(self) -> dto.AvailableDayList:
        # try:
        db_day_list: List[database.AvailableDay] = (
            await self.session.scalars(
                select(database.AvailableDay)
                .order_by(database.AvailableDay.day)
            )
        )
        # except:
            
        
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
