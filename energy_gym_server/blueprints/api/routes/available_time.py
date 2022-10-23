from flask import request, jsonify

from .. import api
from energy_gym_server.services import AvailableTimeService, AuthorizationService
from energy_gym_server.models import dto, AccesRights


@api.get('/available-time/get-list')
@AuthorizationService.check_acces(AccesRights.AVAILABLETIME.GET)
def get_available_day_list():
    with AvailableTimeService() as service:
        data = service.get_all_days()
    return jsonify(data.dict())


# @api.get('/available-time/get-list-in-period')
# @AuthorizationService.check_acces(AccesRights.AVAILABLETIME.GET)
# def get_available_day_list_in_period():
#     request_dto = dto.AvailableTimeListInPeriodRequest(**request.json)

#     with AvailableTimeService() as service:
#         data = service.get_days_by_period(request_dto)

#     return jsonify(data.dict())


@api.get('available-time/get-by-code')
@AuthorizationService.check_acces(AccesRights.AVAILABLETIME.GET)
def get_abailable_day_by_code():
    request_dto = dto.ItemByCodeRequest(**request.json)

    with AvailableTimeService() as service:
        data = service.get_time_by_code(request_dto)

    return jsonify(data.dict())


@api.post('/available-time/add')
@AuthorizationService.check_acces(AccesRights.AVAILABLETIME.ADD)
def add_day():
    request_dto = dto.AvailableTimeAddRequest(**request.json)

    with AvailableTimeService() as service:
        data = service.add_time(request_dto)
        service.commit()

    return jsonify(data.dict())


@api.delete('/available-time/delete')
@AuthorizationService.check_acces(AccesRights.AVAILABLETIME.DELETE)
def delete_available_day():
    request_dto = dto.ItemDeleteRequest(**request.json)

    with AvailableTimeService() as service:
        data = service.delete_day(request_dto)
        service.commit()

    return jsonify(data.dict())
