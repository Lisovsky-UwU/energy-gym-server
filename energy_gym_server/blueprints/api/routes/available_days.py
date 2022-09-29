from quart import request, jsonify

from .. import api
from energy_gym_server import services
from energy_gym_server.models import dto


@api.get('/available-days/get-list')
async def get_available_day_list():
    async with services.AvailableDaysService() as service:
        data = await service.get_all_days()

    return jsonify(data.dict())


@api.post('/available-days/add-day')
async def add_day():
    body = await request.get_json()
    request_dto = dto.AvailableDayAddRequest(**body)

    async with services.AvailableDaysService() as service:
        day = await service.add_day(request_dto)
        await service.commit()

    return jsonify(day.dict())
