from flask import request, jsonify

from .. import api
from energy_gym_server.services import AvailableDaysService, AuthorizationService
from energy_gym_server.models import dto, AccesRights


@api.get('/available-days/get-list')
@AuthorizationService.check_acces(AccesRights.AVAILABLEDAY.GET)
def get_available_day_list():
    with AvailableDaysService() as service:
        data = service.get_all_days()
    return jsonify(data.dict())


@api.get('/available-days/get-list-in-period')
@AuthorizationService.check_acces(AccesRights.AVAILABLEDAY.GET)
def get_available_day_list_in_period():
    request_dto = dto.AvailableDayListInPeriodRequest(**request.json)

    with AvailableDaysService() as service:
        data = service.get_days_by_period(request_dto)

    return jsonify(data.dict())


@api.get('available-days/get-by-code')
@AuthorizationService.check_acces(AccesRights.AVAILABLEDAY.GET)
def get_abailable_day_by_code():
    request_dto = dto.ItemByCodeRequest(**request.json)

    with AvailableDaysService() as service:
        data = service.get_day_by_code(request_dto)

    return jsonify(data.dict())


@api.post('/available-days/add')
@AuthorizationService.check_acces(AccesRights.AVAILABLEDAY.ADD)
def add_day():
    request_dto = dto.AvailableDayAddRequest(**request.json)

    with AvailableDaysService() as service:
        data = service.add_day(request_dto)
        service.commit()

    return jsonify(data.dict())


@api.delete('/available-days/delete')
@AuthorizationService.check_acces(AccesRights.AVAILABLEDAY.DELETE)
def delete_available_day():
    request_dto = dto.ItemDeleteRequest(**request.json)

    with AvailableDaysService() as service:
        data = service.delete_day(request_dto)
        service.commit()

    return jsonify(data.dict())
