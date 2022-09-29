from quart import request, jsonify

from .. import api
from energy_gym_server.services import AvailableDaysService
from energy_gym_server.models import dto


@api.get('/available-days/get-list')
async def get_available_day_list():
    async with AvailableDaysService() as service:
        data = await service.get_all_days()

    return jsonify(data.dict())


@api.post('/available-days/add-day')
async def add_day():
    body = await request.get_json()
    request_dto = dto.AvailableDayAddRequest(**body)

    async with AvailableDaysService() as service:
        data = await service.add_day(request_dto)
        await service.commit()

    return jsonify(data.dict())


@api.get('/available-days/get-list-in-period')
async def get_available_day_list_in_period():
    body = await request.get_json()
    request_dto = dto.AvailableDaysInPeriodRequest(**body)

    async with AvailableDaysService() as service:
        data = await service.get_days_by_period(request_dto)

    return jsonify(data.dict())