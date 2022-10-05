from quart import request, jsonify
from dependency_injector.wiring import Provide, inject

from .. import api
from energy_gym_server.services import AvailableDaysService
from energy_gym_server.models import dto
from energy_gym_server.containers import Application


@api.get('/available-days/get-list')
@inject
async def get_available_day_list(
    service: AvailableDaysService = Provide[Application.services.available_day]
):
    data = await service.get_all_days()
    return jsonify(data.dict())


@api.get('/available-days/get-list-in-period')
@inject
async def get_available_day_list_in_period(
    service: AvailableDaysService = Provide[Application.services.available_day]
):
    body = await request.get_json()
    request_dto = dto.AvailableDayListInPeriodRequest(**body)

    data = await service.get_days_by_period(request_dto)

    return jsonify(data.dict())


@api.get('available-days/get-by-code')
@inject
async def get_abailable_day_by_code(
    service: AvailableDaysService = Provide[Application.services.available_day]
):
    body = await request.get_json()
    request_dto = dto.ItemByCodeRequest(**body)

    data = await service.get_day_by_code(request_dto)

    return jsonify(data.dict())


@api.post('/available-days/add')
@inject
async def add_day(
    service: AvailableDaysService = Provide[Application.services.available_day]
):
    body = await request.get_json()
    request_dto = dto.AvailableDayAddRequest(**body)

    data = await service.add_day(request_dto)
    await service.commit()

    return jsonify(data.dict())


@api.delete('/available-days/delete')
@inject
async def delete_available_day(
    service: AvailableDaysService = Provide[Application.services.available_day]
):
    body = await request.get_json()
    request_dto = dto.ItemsDeleteRequest(**body)

    data = await service.delete_day(request_dto)
    await service.commit()

    return jsonify(data.dict())
